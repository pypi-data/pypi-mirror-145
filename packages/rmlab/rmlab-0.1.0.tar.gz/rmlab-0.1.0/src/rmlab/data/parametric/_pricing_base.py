from dataclasses import dataclass
from rmlab._data.enums import FileExtensions, PricingModelKind
from rmlab.data.items import PModel


@dataclass
class PricingModel(PModel):
    """Pricing models docstring"""

    kind: PricingModelKind
    extension: FileExtensions
