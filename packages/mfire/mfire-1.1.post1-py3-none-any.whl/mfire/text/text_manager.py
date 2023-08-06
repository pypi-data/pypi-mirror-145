from typing import Union

from pydantic import BaseModel

from mfire.composite.components import RiskComponentComposite, TextComponentComposite
from mfire.text.comment_manager import CommentManager
from mfire.text.generator import TextGenerator


class TextManager(BaseModel):
    """Class for dispatching the text generation according to the given component's
    type.

    Args:
        component (Union[RiskComponentComposite, TextComponentComposite]) :
            Component to produce a text with.
    """

    component: Union[RiskComponentComposite, TextComponentComposite]

    def compute(self, geo_id: str = None) -> str:
        """Produce a text according to the given self.component's type.

        Args:
            geo_id (str, optional): Optional geo_id for comment generation.
                Defaults to None.

        Returns:
            str: Text corresponding to the self.component and the given GeoId.
        """
        if isinstance(self.component, TextComponentComposite):
            manager = TextGenerator(**self.component.dict())
            return manager.generate()
        manager = CommentManager(component=self.component)
        return manager.get_comment(geo_id=geo_id)
