"""
    Module d'interprétation de la configuration des geos
"""

from pydantic import root_validator
from typing import List, Optional, Union
import xarray as xr

from mfire.settings import get_logger
from mfire.utils.xr_utils import Loader, ArrayLoader
from mfire.data.aggregator import Aggregator
from mfire.composite.base import BaseComposite
from mfire.composite.aggregations import Aggregation, AggregationType
from mfire.composite.operators import LogicalOperator
from mfire.composite.geos import GeoComposite
from mfire.composite.events import EventComposite, EventBertrandComposite


# Logging
LOGGER = get_logger(name="levels.mod", bind="level")


class LevelComposite(BaseComposite):
    """Création d'un objet level contenant la configuration des levels
    de la tâche de production promethee

    Args:
        baseModel : modèle de la librairie pydantic

    Returns:
        baseModel : objet Level
    """

    level: int
    aggregation: Optional[Aggregation]
    probability: str
    elements_event: List[Union[EventBertrandComposite, EventComposite]]
    logical_op_list: Optional[List[str]]
    aggregation_type: AggregationType
    geos: Optional[GeoComposite]
    altitude_file: Optional[str]
    alt_min: Optional[int]
    alt_max: Optional[int]
    time_dimension: Optional[str]
    compute_list: Optional[list]
    compass_split: Optional[bool]
    altitude_split: Optional[bool]
    geos_descriptive: Optional[List[str]]
    _spatial_risk_da: xr.DataArray = xr.DataArray()
    _mask_da: xr.DataArray = None

    @root_validator(pre=True)
    def init_aggregation_aval(cls, values):
        # ! temporary : utilisation d'alias
        aliases = (
            ("elements_event", "elementsEvent"),
            ("logical_op_list", "logicalOpList"),
            ("aggregation_type", "aggregationType"),
        )
        for attr, alias in aliases:
            if alias in values and attr not in values:
                values[attr] = values.pop(alias)

        # compute list
        if values.get("compute_list") is None:
            values["compute_list"] = ["density", "extrema", "representative", "summary"]

        # coherence len(elements_event) et len(logical_op_list)
        elements_event = values.get("elements_event")
        logical_op_list = values.get("logical_op_list", [])
        if len(logical_op_list) != len(elements_event) - 1:
            raise AttributeError(
                f"The number of logical operator ({len(logical_op_list)})"
                " is not consistent with the len of element list"
                f"(n={len(elements_event)}. Should be {len(elements_event)-1}."
            )

        # cohérence aggregation et aggregation_type
        agg_type = values.get("aggregation_type")
        if values.get("aggregation") and agg_type == AggregationType.UP_STREAM:
            # là on force le l'aggregation à None
            values["aggregation"] = None
        if (
            values.get("aggregation") is None
            and agg_type == AggregationType.DOWN_STREAM
        ):
            raise ValueError("Missing expected value 'aggregation' in level")

        # propagation des aggregation, geos et altitude au elements
        for i in range(len(elements_event)):
            element = elements_event[i]
            if isinstance(element, EventComposite):
                element = element.dict()
            element["aggregation_aval"] = values.get("aggregation")
            element["geos"] = values.get("geos")
            element["alt_max"] = values.get("alt_max")
            element["alt_min"] = values.get("alt_min")
            element["geos_descriptive"] = values.get("geos_descriptive")
            element["compass_split"] = values.get("compass_split")
            element["altitude_split"] = values.get("altitude_split")
            element["time_dimension"] = values.get("time_dimension")
            element["altitude_file"] = values.get("altitude_file")

            if (
                element.get("aggregation") is None
                and agg_type == AggregationType.UP_STREAM
            ):
                # ici on force l'aggregation par la moyenne dans l'element
                element["aggregation"] = Aggregation(method="mean")
            if element.get("aggregation") and agg_type == AggregationType.DOWN_STREAM:
                # ici on force l'aggregation de l'element à None
                element["aggregation"] = None

            elements_event[i] = element

        return values

    @property
    def mask_da(self) -> xr.DataArray:
        if self._mask_da is None:
            mask_list = []
            for i, evt in enumerate(self.elements_event):
                if isinstance(evt.geos, xr.DataArray):  # ! temporary #GeoGate
                    geo_da = evt.geos
                elif isinstance(evt.geos, GeoComposite):  # ! temporary #GeoGate
                    if evt.geos.grid_name is None:
                        evt.field.compute()
                        # ! temporairement on assigne le grid_name comme ça
                        evt.geos.grid_name = evt.field.get_grid_name()
                    geo_da = evt.geos.compute()
                mask_list.append(geo_da.expand_dims("place").assign_coords(place=[i]))
            self._mask_da = xr.concat(mask_list, dim="place").max(dim="place")
        return self._mask_da

    @property
    def spatial_risk_da(self) -> xr.DataArray:
        return self._spatial_risk_da

    @property
    def _cached_attrs(self) -> dict:
        return {
            "data": Loader,
            "spatial_risk_da": ArrayLoader,
            "mask_da": ArrayLoader,
        }

    def _compute(self) -> xr.Dataset:
        global LOGGER
        LOGGER = LOGGER.bind(level=self.level, composite_hash=self.hash)
        # ! start temporary patch : ref #GeoGate
        if isinstance(self.geos, xr.DataArray):
            LOGGER = LOGGER.bind(geo="localised dataarray (unnamed)")
        else:
            LOGGER = LOGGER.bind(geo=self.geos.file)
        # ! end temporary patch : ref #GeoGate
        LOGGER.debug("Launching level.compute_risk")
        output_ds = self._compute_risk()
        LOGGER.debug("level.compute_risk done")
        LOGGER.try_unbind("level", "geo", "composite_hash")
        return output_ds

    def get_singleEvt_comparison(self) -> Union[dict, None]:
        """
        Enable to get, for a single event, the comparison operator

        Returns:
            Union[dict, None]: A list of comparison operator.
                None if there is several event.
        """
        res = None
        if len(self.elements_event) == 1:
            res = self.elements_event[0].get_comparison()
        else:
            #  On verifie que les evenement dans la liste ne sont pas identique,
            # i-e ils différent seulement par les chemins de fichiers.
            evt0 = self.elements_event[0]
            all_the_same = True
            for evt in self.elements_event:
                if evt != evt0:
                    all_the_same = False
            if all_the_same:
                res = self.elements_event[0].get_comparison()
        return res

    def get_comparison(self) -> Union[dict, None]:
        dout = dict()
        for event in self.elements_event:
            field = event.field.get_name()
            comparison = event.get_comparison()
            if field is not None and field not in dout:
                dout[field] = comparison
            elif field in dout and dout[field] != comparison:
                LOGGER.error(
                    f" Current  {dout[field]} is different of new one {comparison}. "
                    "Don't know what to do in this case. "
                )
        return dout

    def get_cover_period(self) -> xr.DataArray:
        return self.elements_event[0].get_cover_period()

    def is_bertrand(self) -> bool:
        """Check if an event of the list is Bertrand Kind."""
        return all(
            isinstance(event, EventBertrandComposite) for event in self.elements_event
        )

    def update_selection(
        self,
        sel: dict = dict(),
        slice: dict = dict(),
        isel: dict = dict(),
        islice: dict = dict(),
    ):
        for element in self.elements_event:
            element.update_selection(sel=sel, slice=slice, isel=isel, islice=islice)

    def get_grid_name(self) -> str:
        """We here make the hypothesis that all file are based on the same grid"""
        return self.elements_event[0].field.get_grid_name()

    def _compute_risk(self) -> xr.Dataset:
        """ Fonction qui calcul un niveau de risque.
        Cette fonction combine différents évènements.
        Le dataset de sortie n'est par contre pas généré. Seul le risque est ici fait.
        """
        output_ds = xr.Dataset()
        # 1. computing all events and retrieving results for output
        events = []
        for i, event in enumerate(self.elements_event):
            events.append(event.compute())
            tmp_ds = event.values_ds.expand_dims(dim="evt").assign_coords(evt=[i])
            output_ds = xr.merge([output_ds, tmp_ds])
        # 2. combining all events using logical operators
        risk_da = LogicalOperator.apply(self.logical_op_list, events)
        self._spatial_risk_da = risk_da * self.mask_da
        # 3. aggregating if necessary
        aggregation = self.aggregation
        if aggregation is not None:
            agg_handler = Aggregator(self._spatial_risk_da)
            # Ajout pour avoir la densite de l'evenement combine en sortie
            if "density" in self.compute_list:
                output_ds["risk_density"] = agg_handler.compute("density")

            if "summary" in self.compute_list:
                agg_handler_time = Aggregator(
                    risk_da, aggregate_dim=self.time_dimension
                )
                max_risk_da = agg_handler_time.compute("max") * self.mask_da
                agg_handler_space = Aggregator(max_risk_da)
                output_ds["risk_summarized_density"] = agg_handler_space.compute(
                    "density"
                )

            # On calcule maintenant l'occurrence du risque
            aggregation_kwargs = dict(aggregation.kwargs or {})
            aggregation_algo = aggregation.method
            risk_da = agg_handler.compute(aggregation_algo, **aggregation_kwargs)

        output_ds["occurrence"] = risk_da
        # On check que les variables sont bien presentes.
        if hasattr(self.mask_da, "label"):
            output_ds["areaName"] = self.mask_da["label"]
        if hasattr(self.mask_da, "areaName"):
            output_ds["areaName"] = self.mask_da["areaName"]
        else:
            output_ds["areaName"] = (
                "id",
                ["unknown" for _ in range(self.mask_da.id.size)],
            )
        if hasattr(self.mask_da, "type"):
            output_ds["areaType"] = self.mask_da["type"]
        if hasattr(self.mask_da, "areaType"):
            output_ds["areaType"] = self.mask_da["areaType"]
        else:
            output_ds["areaType"] = (
                "id",
                ["unknown" for _ in range(self.mask_da.id.size)],
            )
        return output_ds.squeeze("tmp")
