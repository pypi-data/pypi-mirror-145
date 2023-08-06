"""Script exposing enumeration types and values to add a type/value-safe 
layer for correctness."""

from enum import Enum


class LowerStringEnumValues(Enum):
    @classmethod
    def str_to_enum_value(cls, v: str):
        return cls.__dict__["_value2member_map_"][v.lower()]


class FileExtensions(LowerStringEnumValues):
    """All possible extensions of uploadable files"""

    JSON = ".json"
    CSV = ".csv"


class DataRemoveKind(LowerStringEnumValues):
    COMPLETE = "full"
    HISTORIC = "restart"


class CurrencyKind(LowerStringEnumValues):
    """All recognized currencies"""

    CROATIAN_KUNA = "hrk"
    CZECH_KORUNA = "czk"
    DANISH_KRONE = "dkk"
    EURO = "eur"
    HUNGARIAN_FORINT = "hug"
    MOLDOVAN_KEY = "mdl"
    NORWEGIAN_KRONE = "nok"
    POLISH_ZLOTY = "pln"
    POUND_STERLING = "gbp"
    SWEDISH_KRONA = "sek"
    SWISS_FRANC = "chf"
    UKRAINIAN_HRYVNIA = "uah"
    US_DOLLAR = "usd"


class ParametricModelKind(LowerStringEnumValues):
    """All possible enumerations for types of parametric models"""

    CUSTOMERS = "customers"
    PRICING = "pricing"


class CustomersModelKind(LowerStringEnumValues):
    """All possible enumerations for types of customers models"""

    REQUEST = "request"
    CHOICE = "choice"


class PricingModelKind(LowerStringEnumValues):
    """All possible enumerations for types of pricing models"""

    RANGE = "range"
    BEHAVIOR = "behavior"
    OPTIMIZER = "optimizer"


class DayOfWeek(Enum):
    """Days of week enumeration"""

    MONDAY = 1
    TUESTDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    @classmethod
    def int_to_enum_value(cls, v: int):
        return cls.__dict__["_value2member_map_"][v]


class ScenarioDayStatus(LowerStringEnumValues):
    """All possible enumerations of daily status"""

    EMPTY = "empty"
    STARTED = "started"
    ENDED = "ended"
    IN_PROGRESS = "inprogress"
    READY = "ready"
    PAUSED = "paused"
    SIMULATED = "simulated"
    OPTIMIZED = "optimized"


class ScenarioState(LowerStringEnumValues):
    """All possible enumerations of scenario states"""

    EMPTY = "empty"
    IN_PROGRESS = "inprogress"
    PAUSED = "paused"
    FINISHED = "finished"


class FlightDataKind(LowerStringEnumValues):
    """All possible enumerations for types of flight data"""

    ACTUAL_BOOKS = "actual-books"
    EXPECTED_BOOKS = "expected-books"
    DYNAMIC_BOOKS = "dynamic-books"
    THRESHOLDS_SETTINGS = "thresholds-settings"
    PRICE_PER_SEAT_SETTINGS = "pps-settings"
    EVENTS = "events"


class FlightEvent(LowerStringEnumValues):
    """All possible enumerations for flight events"""

    FLIGHT_LOADED = "flight-loaded"
    FLIGHT_DEPARTED = "flight-departed"
    FLIGHT_SOLD_OUT = "flight-sold-out"
    SCHEDULED_OPT_PASS = "scheduled-rms-pass"
    DONE_OPT_PASS = "done-rms-pass"
    COMMIT_OPT_PASS = "commit-rms-pass"
    LOADED_INITIAL_THRESHOLDS = "loaded-initial-thresholds"
    OPERATOR_EDIT_THRESHOLDS = "operator-edit-thresholds"
    OPERATOR_DYNAMIC_TO_EXPECTED = "operator-dynamic-to-expected"


class OptimizationSelectorFilterKind(LowerStringEnumValues):
    """All possible enumerations for optimization selector kinds."""

    DAY_OF_WEEK = "day-of-week"
    HOUR_SLOT = "hour-slot"
    SECTOR = "sector"
    SCHEDULE = "schedule"
    FLIGHT_NUMBER = "flight-number"
    SEAT_CAPACITY = "seat-capacity"


class TimeUnit(Enum):
    """Enumerations for time units in optimization selector."""

    DAY = "day"
    MONTH = "month"
    YEAR = "year"

    @classmethod
    def str_to_enum_value(cls, v: str):
        # Make it case-insensitive
        v = v.lower()
        if v[-1] == "s":  # Make it singular
            v = v[0:-1]
        return cls.__dict__["_value2member_map_"][v]


class OptimizationForecasterKind(LowerStringEnumValues):
    """All implemented forecaster kinds."""

    Q_FORECAST = "q-forecast"
    BAYES = "bayes"


class OptimizationAggregatorKind(LowerStringEnumValues):
    """All implemented ways to aggregate historic data."""

    UNIFORM = "uniform"
    EXPONENTIAL = "exponential"


class OptimizationMaximizerKind(LowerStringEnumValues):
    """All implemented revenue maximization algorithms."""

    DP_QSD = "qsd"


class OptimizationEffectsKind(LowerStringEnumValues):
    """All implemented post-optimization effects."""

    NONE = "none"
    COMMIT_THRESHOLDS = "commit"


class ParametricFilterClassKind(LowerStringEnumValues):
    """All implemented filter class kinds."""

    IN_PERIOD = "in_period"
    FLIGHT_NUMBER = "flight_number"
    AIRLINE = "airline"
    SECTOR = "sector"
    ROUTE = "route"
    CITYSECTOR = "citysector"
    CITYROUTE = "cityroute"
    NETWORK = "network"
