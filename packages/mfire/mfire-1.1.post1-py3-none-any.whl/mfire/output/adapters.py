"""mfire.output module OutputAdapter
"""

from pydantic import Field

from mfire.output.base import BaseOutputAdapter, BaseOutputProduction
from mfire.output.cdp import CDPRiskAdapter, CDPTextAdapter


class OutputAdapter(BaseOutputAdapter):
    """ Base class to be used for the implementation of an adapter
    taking a risk or text component

    Args:
        BaseModel : BaseOutputAdapter

    Returns:
        BaseModel : BaseOutputProduction
    """

    output_type: str = Field("factory", const=True)

    def compute(self) -> BaseOutputProduction:
        adapter = CDPRiskAdapter(component=self.component, texts=self.texts)
        if self.component.type in ("text", "Text"):
            adapter = CDPTextAdapter(component=self.component, texts=self.texts)
        return adapter.compute()
