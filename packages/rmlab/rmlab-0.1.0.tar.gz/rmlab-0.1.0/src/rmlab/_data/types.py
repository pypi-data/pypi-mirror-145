"""Internal types

Script exposing auxiliary global variables, functions and types to 
provide a minimal typed structure to items.
"""

from dataclasses import dataclass, fields, is_dataclass
from typing import List
import inspect


DateFormat = "%Y-%m-%d"
DateTimeMinFormat = "%Y-%m-%dT%H:%M"
DateTimeSecFormat = "%Y-%m-%dT%H:%M:%S"
DateTimeMicroSecFormat = "%Y-%m-%dT%H:%M:%S.%f"


@dataclass
class APIEvent:
    event: str
    timestamp: int

    def __post_init__(self):
        self.timestamp = int(self.timestamp)


@dataclass
class Item:
    """Base class for all Item classes"""

    id: str


@dataclass
class CustomersModelHolder:
    """Item associated with specific customers models"""

    crequest_id: str
    cchoice_id: str


@dataclass
class PricingModelHolder:
    """Item associated with specific pricing models"""

    prange_id: str
    pbehavior_id: str
    poptimizer_id: str


class CoreItem:
    """Item initialized from direct data upload"""

    pass


class DerivedItem:
    """Item initialized from other item categories"""

    pass


class AirlineLocation:
    """Item that is location attribute of an airline"""

    pass


class BoundedItem(Item):
    """Item whose elements are bounded. The amount of unbounded items grows with the size/space of the underlying scenario"""

    pass


class UnboundedItem(Item):
    """Item whose elements are unbounded. The amount of unbounded items grows with the time period of the underlying scenario, which is in general unlimited"""

    pass


def fields_of_dataclass(category: type) -> List[str]:
    """Return the fields of a dataclass as a list of strings.

    Args:
        category (type): Class of any category

    Returns:
        List of fields as strings
    """

    flds = set()

    for base_class in inspect.getmro(category):
        if is_dataclass(base_class):
            flds.update({f.name for f in fields(base_class)})

    return list(flds)
