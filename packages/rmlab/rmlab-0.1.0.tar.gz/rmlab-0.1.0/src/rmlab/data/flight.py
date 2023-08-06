"""
This script provides dataclasses storing arrays representing temporal data of flights.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Mapping

from rmlab._data.enums import FlightEvent


@dataclass
class FlightData:
    """Base dataclass for derived classes holding time series data associated to a flight.

    Args:
        id (str): Flight ID to which time series data arrays are associated
        timestamps_array (List[datetime]): Sequence of time stamps with milliseconds granularity
    """

    id: str
    timestamps_array: List[datetime]

    def __post_init__(self):
        # NOTE input timestamps are in millisec
        self.timestamps_array = [
            datetime.utcfromtimestamp(ts / 1000) for ts in self.timestamps_array
        ]

    def is_empty(self):
        return len(self.timestamps_array) == 0


@dataclass
class FlightDataBooks(FlightData):
    """Data class with arrays related to books associated to a flight

    Args:
        fares_array (List[str]): Stores the enabled fares at each time stamp
        pps_array (List[int]): Stores the price per seat associated to each booking
        seats_array (List[int]): Stores the seats booked for each booking
        cumulated_seats_array (List[int]): Stores the cumulated booked seats at each time stamp
        cumulated_revenue_array (List[int]): Stores the cumulated revenue at each time stamp
    """

    fares_array: List[str]
    pps_array: List[int]
    seats_array: List[int]
    cumulated_seats_array: List[int]
    cumulated_revenue_array: List[int]


@dataclass
class FlightDataForecastedBooks(FlightData):
    """Data class with arrays related to forecasted books associated to a flight

    Args:
        pps_array (List[int]): Stores the forecasted price per seat at each time stamp
        seats_array (List[int]): Stores the forecasted cumulated booked seats at each time stamp
    """

    pps_array: List[int]
    seats_array: List[int]


@dataclass
class FlightDataThresholdSettings(FlightData):
    """Data class with arrays of seat thresholds for each fare associated to a flight

    Args:
        fare_to_threshold_array (Mapping[str], List[int]): Maps each fare identifier
            to an array storing the seat thresholds at each time stamp.
    """

    fare_to_threshold_array: Mapping[str, List[int]]


@dataclass
class FlightDataPricePerSeatSettings(FlightData):
    """Data class with arrays of prices per seat for each fare associated to a flight

    Args:
        fare_to_pps_array (Mapping[str], List[int]): Maps each fare identifier
            to an array storing the prices per seat at each time stamp.
    """

    fare_to_pps_array: Mapping[str, List[int]]


@dataclass
class FlightDataEvents(FlightData):
    """Data class holding a sequence of events associated to a flight

    Args:
        events_array (List[FlightEvent]): Stores the events at each time stamp.
    """

    events_array: List[FlightEvent]
