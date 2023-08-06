"""
This script provides dataclasses that represent a global information of scenarios.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from rmlab._data.enums import ScenarioDayStatus, ScenarioState
from rmlab._data.types import DateFormat, DateTimeSecFormat


@dataclass
class Scenario:
    """Base class for dataclasses holding per-scenario information.

    Args:
        id (int): Scenario identifier

    """

    id: int

    def __post_init__(self):
        self.id = int(self.id)

    def __repr__(self) -> str:
        return self.__dict__


@dataclass
class ScenarioDates(Scenario):
    """Set of dates and status characteristic to a scenario.

    Args:
        day_status (ScenarioDayStatus): Intra day scenario status
        current (datetime): Current date upto days (year-month-day)
        next (datetime): Date at which simulation would stop, upto days (year-month-day)
        first_flight_load (datetime): Date at which the first flight is put on sale, upto days (year-month-day)
        last_flight_departure (datetime): Date at which the last flight departs, upto days (year-month-day)
        checkpoints (datetime): List of dates at which simulation would stop, upto days (year-month-day)
        state (ScenarioState): Global state of scenario
    """

    day_status: ScenarioDayStatus
    current: datetime
    next: datetime
    first_flight_load: datetime
    last_flight_departure: datetime
    checkpoints: List[datetime]
    upload_time: datetime
    state: ScenarioState

    def __post_init__(self):

        self.day_status = ScenarioDayStatus.str_to_enum_value(self.day_status)
        self.current = datetime.strptime(self.current, DateFormat)
        self.next = datetime.strptime(self.next, DateFormat)
        self.first_flight_load = datetime.strptime(self.first_flight_load, DateFormat)
        self.last_flight_departure = datetime.strptime(
            self.last_flight_departure, DateFormat
        )
        self.checkpoints = [
            datetime.strptime(chp, DateFormat) for chp in self.checkpoints
        ]
        self.upload_time = datetime.strptime(self.upload_time, DateTimeSecFormat)


@dataclass
class ItemsCount(Scenario):
    """Counters of items of bounded categories.

    Args:
        aircraft (int): Number of referenced aircrafts in scenario
        airline (int): Number of referenced airlines in scenario
        airport (int): Number of referenced airports in scenario
        city (int): Number of referenced cities in scenario
        country (int): Number of referenced countries in scenario
        cityroute (int): Number of cityroutes in scenario
        citysector (int): Number of citysectors in scenario
        route (int): Number of routes in scenario
        sector (int): Number of sectors in scenario
        pmodel (int): Number of parametric models in scenario
    """

    aircraft: int
    airline: int
    airport: int
    city: int
    cityroute: int
    citysector: int
    country: int
    pmodel: int
    route: int
    sector: int


@dataclass
class SchedulesCount(Scenario):
    """Counters of flights schedules in a given scenario.

    Args:
        past (int): Number of schedules with all flights departed at current date
        live (int): Number of schedules with flights on sale at current date
        pending (int): Number of schedules with all flights not yet on sale at current date
        total (int): Total number of schedules
    """

    past: int
    live: int
    pending: int
    total: int = field(init=False)

    def __post_init__(self):
        self.total = self.past + self.live + self.pending


@dataclass
class FlightsCount(Scenario):
    """Counters of flights in a given scenario.

    Args:
        past (int): Number of flights departed at current date
        live (int): Number of flights on sale at current date
        pending (int): Number of flights not departed and not yet on sale at current date
        total (int): Total number of flights (schedules)
    """

    past: int
    live: int
    pending: int
    total: int = field(init=False)

    def __post_init__(self):
        self.total = self.past + self.live + self.pending
