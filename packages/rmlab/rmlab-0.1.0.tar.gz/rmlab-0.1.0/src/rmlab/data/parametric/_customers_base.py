from dataclasses import dataclass
from rmlab._data.enums import CustomersModelKind, FileExtensions
from rmlab.data.items import PModel


@dataclass
class CustomersModel(PModel):
    """Customers models docstring"""

    kind: CustomersModelKind
    extension: FileExtensions
