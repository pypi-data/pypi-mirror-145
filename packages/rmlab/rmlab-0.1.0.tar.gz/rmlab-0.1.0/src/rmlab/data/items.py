"""
This script provides dataclasses that represent the relational data components in the server.
"""

from typing import List, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import importlib
import inspect
from rmlab._data.enums import CurrencyKind, DayOfWeek

from rmlab._data.types import (
    AirlineLocation,
    BoundedItem,
    CoreItem,
    CustomersModelHolder,
    DateFormat,
    DateTimeMinFormat,
    DerivedItem,
    PricingModelHolder,
    UnboundedItem,
)


@dataclass
class PModel(BoundedItem, CoreItem):
    """Item holding a set of parameters.

    Args:
        filename (str): Name of file storing the parameters
        hash (str): MD5 hash of the content
        cnt (str): Model content
    """

    filename: str
    hash: str
    cnt: str


@dataclass
class Airline(BoundedItem, CoreItem):
    """Airline instance.

    Args:
        name (str): Airline name and ID
        type (str): Airline type (Either 'low-cost' or 'legacy')
    """

    name: str
    type: str = "undefined"


@dataclass
class Aircraft(BoundedItem, CoreItem):
    """Aircraft instance.

    Args:
        model (str): Aircraft model and ID
        seat_capacity (int): Seat capacity
    """

    model: str
    seat_capacity: int

    def __post_init__(self):
        self.seat_capacity = int(self.seat_capacity)


@dataclass
class Country(BoundedItem, CoreItem):
    """Country instance.

    Args:
        name (str): Country name and ID
        currency (CurrencyKind): Country currency
    """

    name: str
    currency: CurrencyKind

    def __post_init__(self):
        if isinstance(self.currency, str):
            self.currency = CurrencyKind.str_to_enum_value(self.currency)


@dataclass
class City(BoundedItem, CoreItem):
    """City instance.

    Args:
        name (str): City name and ID
        country_id (str): Country ID of the city
    """

    name: str
    country_id: str


@dataclass
class CitySector(BoundedItem, DerivedItem, CustomersModelHolder, AirlineLocation):
    """Pair of cities with specified direction.

    Args:
        origin_id (str): Departure city ID
        destination_id (str): Arrival city ID
    """

    origin_id: str
    destination_id: str


@dataclass
class CityRoute(BoundedItem, DerivedItem, CustomersModelHolder, AirlineLocation):
    """Pair of cities with unspecified direction.

    Args:
        first_id (str): First city ID of the pair in alphabetical order
        second_id (str): Second city ID of the pair in alphabetical order
    """

    first_id: str
    second_id: str


@dataclass
class Airport(BoundedItem, CoreItem):
    """Airport instance.

    Args:
        name (str): Full airport name
        city_id (str): City ID of the airport
        iata (str): IATA code of the airport
        icao (str): ICAO code of the airport
        altitude (int): Location altitude in MAMSL
        latitude (int): Location latitude
        longitude (int): Location longitude
    """

    name: str
    city_id: str
    iata: str
    icao: str = "undefined"
    altitude: int = 0
    latitude: int = 0
    longitude: int = 0

    def __post_init__(self):
        self.altitude = int(self.altitude)
        self.latitude = int(self.latitude)
        self.longitude = int(self.longitude)


@dataclass
class Sector(BoundedItem, DerivedItem, AirlineLocation):
    """Pair of airports with specified direction.

    Args:
        origin_id (str): Departure airport ID
        destination_id (str): Arrival airport ID
    """

    origin_id: str
    destination_id: str
    citysector_id: str


@dataclass
class Route(BoundedItem, DerivedItem, AirlineLocation):
    """Pair of airports with unspecified direction.

    Args:
        first_id (str): First airport ID of the pair in alphabetical order
        second_id (str): Second airport ID of the pair in alphabetical order
    """

    first_id: str
    second_id: str
    cityroute_id: str


@dataclass
class Schedule(UnboundedItem, CoreItem):
    """Schedule instance. Template generator for flights in an airline with common aircraft, sector and days of week.

    Args:
        airline_id (str): Airline ID
        aircraft_id (str): Aircraft ID
        origin_id (str): Departure airport ID
        destination_id (str): Arrival airport ID
        days_of_week (List[DayOfWeek]): Days of week
        departure_time (timedelta): Departure time upto minutes (hour-minutes)
        duration (timedelta): Flight duration upto minutes (hour-minutes)
        flight_number (int): Flight number identifier
        sell_before_days (int): Flights are put on sale these days before departure day
        from_date (datetime): Start date of the range of flight departures, upto days (year-month-day)
        to_date (datetime): End date of the range of flight departures, up to days (year-month-day)
        sector_id (str): Sector ID
        citysector_id (str): CitySector ID
        route_id (str): Route ID
        cityroute_id (str): CityRoute ID
        from_date_load (datetime): Start date of the selling period, upto days (year-month-day)
        to_date_load (datetime): End date of the selling period, upto days (year-month-day)
        from_date_departure (datetime): Date of the first departure, upto days (year-month-day)
        to_date_departure (datetime): Date of the last departure, up to days (year-month-day)

    """

    airline_id: str
    aircraft_id: str
    origin_id: str
    destination_id: str
    days_of_week: List[DayOfWeek]
    departure_time: timedelta
    duration: int
    flight_number: str
    sell_before_days: int
    from_date: str
    to_date: str
    sector_id: str
    citysector_id: str
    route_id: str
    cityroute_id: str
    from_date_load: datetime
    to_date_load: datetime
    from_date_departure: datetime
    to_date_departure: datetime

    def __post_init__(self):

        self.sell_before_days = int(self.sell_before_days)

        self.days_of_week = [
            DayOfWeek.int_to_enum_value(int(d))
            for d in self.days_of_week.replace("-", "")
        ]
        self.departure_time = self.departure_time

        self.from_date = datetime.strptime(self.from_date, DateFormat)
        self.to_date = datetime.strptime(self.to_date, DateFormat)
        self.from_date_load = datetime.strptime(self.from_date_load, DateFormat)
        self.to_date_load = datetime.strptime(self.to_date_load, DateFormat)
        self.from_date_departure = datetime.strptime(
            self.from_date_departure, DateFormat
        )
        self.to_date_departure = datetime.strptime(self.to_date_departure, DateFormat)

        self.departure_time = timedelta(minutes=int(self.departure_time))
        self.duration = timedelta(minutes=int(self.duration))


@dataclass
class Flight(UnboundedItem, DerivedItem, PricingModelHolder):
    """Flight instance.

    Args:
        seat_capacity (int): Seat capacity
        schedule_id (str): Schedule ID
        sector_id (str): Sector ID
        citysector_id (str): CitySector ID
        airline_id (str): Airline ID
        aircraft_id (str): Aircraft ID
        flight_number (str): Flight number identifier
        onsale_date_time (datetime): Flight is put on sale this date, upto days (year-month-day)
        departure_date_time (datetime): Departure date and time, upto minutes (year-month-day-hour-minute)
        fares (List[str]): List of fare identifiers
        lowest_pps (int): Price per seat of the lowest fare in cents
        highest_pps (int): Price per seat of the highest fare in cents
    """

    seat_capacity: int
    schedule_id: str
    sector_id: str
    citysector_id: str
    airline_id: str
    aircraft_id: str
    flight_number: str
    onsale_date_time: datetime
    departure_date_time: datetime
    fares: List[str]
    lowest_pps: int
    highest_pps: int

    def __post_init__(self):
        self.seat_capacity = int(self.seat_capacity)
        self.fares = self.fares.split("-")
        self.lowest_pps = self.lowest_pps
        self.highest_pps = self.highest_pps
        self.onsale_date_time = datetime.strptime(self.onsale_date_time, DateFormat)
        self.departure_date_time = datetime.strptime(
            self.departure_date_time, DateTimeMinFormat
        )


AnyAirlineLocationType = Union[Sector, CitySector, Route, CityRoute]
AnyBoundedType = Union[
    PModel,
    Airline,
    Aircraft,
    Country,
    City,
    CitySector,
    CityRoute,
    Airport,
    Sector,
    Route,
]
AnyUnboundedType = Union[Schedule, Flight]

AllBoundedItems = [
    obj
    for name, obj in inspect.getmembers(importlib.import_module(__name__))
    if inspect.isclass(obj) and obj != BoundedItem and issubclass(obj, BoundedItem)
]

AllUnboundedItems = [
    obj
    for name, obj in inspect.getmembers(importlib.import_module(__name__))
    if inspect.isclass(obj) and obj != UnboundedItem and issubclass(obj, UnboundedItem)
]

AllCoreItems = [
    obj
    for name, obj in inspect.getmembers(importlib.import_module(__name__))
    if inspect.isclass(obj) and obj != CoreItem and issubclass(obj, CoreItem)
]

AllDerivedItems = [
    obj
    for name, obj in inspect.getmembers(importlib.import_module(__name__))
    if inspect.isclass(obj) and obj != DerivedItem and issubclass(obj, DerivedItem)
]

AirlineLocationItems = [
    obj
    for name, obj in inspect.getmembers(importlib.import_module(__name__))
    if inspect.isclass(obj)
    and obj != AirlineLocation
    and issubclass(obj, AirlineLocation)
]
