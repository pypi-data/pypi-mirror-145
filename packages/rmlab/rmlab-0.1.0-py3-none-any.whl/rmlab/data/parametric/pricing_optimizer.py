"""
A pricing optimizer completely defines the revenue optimization strategy to apply to 
flights. In particular, it is needed to define:

1. A **schedule**, to define *when* to trigger optimization passes.

2. A **selector**, to specify the *inputs* of the optimization passes for each flight.

3. An **operator**, to specify the set of *actions* and *algorithms* that will run on the input data, encompasing:
"""


from dataclasses import dataclass
import json
from typing import Any, List, Mapping, Optional, Union

from rmlab._data.conversions import parse_data_from_json
from rmlab._data.enums import (
    FileExtensions,
    OptimizationAggregatorKind,
    OptimizationEffectsKind,
    OptimizationForecasterKind,
    OptimizationMaximizerKind,
    OptimizationSelectorFilterKind,
    PricingModelKind,
    TimeUnit,
)
from rmlab.data.parametric._pricing_base import PricingModel


@dataclass
class OptimizerSchedule:
    """Optimizer schedule parameters specify when and
    how often optimization passes are triggered.

    Args:
      from_dbd (int): Positive day before departure from which this schedule is applied.
      day_frequency (int): Number of days between consecutive optimization passes

    Examples:

    * Run every 30 days since it is put on sale:
    ```py
    sch = OptimizerSchedule(from_dbd=float('inf'), day_frequency=30)
    ```

    * Run every 15 days when it reaches dbd 180:
    ```py
    sch = OptimizerSchedule(from_dbd=180, day_frequency=15)
    ```

    * Run every 7 days when it reaches dbd 60:
    ```py
    sch = OptimizerSchedule(from_dbd=60, day_frequency=7)
    ```

    * Run every 3 days when it reaches dbd 30:
    ```py
    sch = OptimizerSchedule(from_dbd=30, day_frequency=3)
    ```

    * Run every day when it reaches dbd 15:
    ```py
    sch = OptimizerSchedule(from_dbd=15, day_frequency=1)
    ```

    """

    from_dbd: int
    day_frequency: int


@dataclass
class OptimizerSelector:
    """Optimizer selector parameters specify which historic data is fed to the forecaster.

    From a functional perspective, a OptimizerSelector instance stores
    a set of parameters that define a function:

    (flightInput) → [flight1, flight2, …, flightN]

    Ie: from the OptimizerSelector parameters we know, given a *flightInput*,
    the set of neighboring flights *[flight1, flight2, …, flightN]* on which
    optimization passes are run upon.

    Args:
      since_qty (int): Time qty
      since_unit (TimeUnit): Time unit
      filters (List[OptimizationSelectorFilterKind]): Filters to apply to input flights

    Examples:

    To create a selector that picks the neighboring flights that:

    * Cover the same citysector and same airline (implicitly assumed, no need to specify it)
    * Depart any time within the last 2 years with respect the flight departure date
    * Departing in the same day of week as flightInput
    * Departing in the same hour slot as flightInput
    * Covering the same sector

    then we create the selector instance as:

    ```py
    sel = OptimizerSelector(
      since_qty=2,
      since_unit="year",
      filters=["day-of-week", "hour-slot", "sector"]
      )
    ```

    See `OptimizationSelectorFilterKind` reference of allowed filters.
    """

    since_qty: int
    since_unit: TimeUnit
    filters: List[OptimizationSelectorFilterKind]

    def __post_init__(self):

        if isinstance(self.since_qty, str) and self.since_qty.lower() == "inf":
            self.since_qty = float("inf")
        else:
            self.since_qty = int(self.since_qty)

        if isinstance(self.since_unit, str):
            self.since_unit = TimeUnit.str_to_enum_value(self.since_unit)

        for i, v in enumerate(self.filters):
            if isinstance(v, str):
                self.filters[i] = OptimizationSelectorFilterKind.str_to_enum_value(v)


class OptimizerMaximizer:
    """Base class for maximizers."""

    kind: OptimizationMaximizerKind


@dataclass
class DPQSDMaximizer(OptimizerMaximizer):
    """Parameters of the DPQSD Maximizer.

    Args:
        max_requests_per_day (int): Upper bound in maximum requests per day
        price_points (int): Number of price points
        ebc_samples (int): Number of samples to take from the optimal solution
    """

    max_requests_per_day: int = 50
    price_points: int = 30
    ebc_samples: int = 5


@dataclass
class OptimizerOperator:
    """Optimizer operator parameters specify the forecasting,
    aggregation and maximization algorithms and which actions are
    performed after an optimization pass finishes.

    Args:
      forecaster_type (OptimizationForecasterKind): Forecaster type
      maximizer_type (OptimizationMaximizerKind): Revenue maximizer type
      aggregate_type (OptimizationAggregatorKind): Type of aggregation of historic input data
      aggregate_value (Optional[float]): Numeric parameter of aggregation type
      effects (str): Actions to perform after maximization

    **Example 1**

    To create an operator that:

    1. Runs *q-forecast* forecaster on all input data
    2. Aggregates forecast data of all flights as a *0.5 exponential" weighting
    3. Modify the thresholds of the flight after maximization pass

    we create an operator instance as:

    ```py
    op = OptimizerOperator(
      forecaster_type="q-forecast",
      maximizer=OptimizerMaximizer(...),
      aggregate_type="exponential",
      aggregate_value=0.5
      effects="commit"
    )
    ```


    **Example 2**

    To create an operator that:

    1. Runs *bayesian* forecaster on all input data
    2. Aggregates forecast data of all flights *uniformly*
    3. Do not apply the results to the thresholds

    we create an operator instance as:

    ```py
    op = OptimizerOperator(
      forecaster_type="q-forecast",
      maximizer=OptimizerMaximizer(...),
      aggregate_type="exponential",
      aggregate_value=0.5
      effects="none"
    )
    ```

    """

    forecaster_type: OptimizationForecasterKind
    maximizer: OptimizerMaximizer
    effects: OptimizationEffectsKind
    aggregate_type: OptimizationAggregatorKind
    aggregate_value: Optional[float] = None

    def __post_init__(self):
        if isinstance(self.forecaster_type, str):
            self.forecaster_type = OptimizationForecasterKind.str_to_enum_value(
                self.forecaster_type
            )

        if not isinstance(self.maximizer, OptimizerMaximizer):
            raise TypeError(f"Unexpected type for maximizer")

        if isinstance(self.aggregate_type, str):
            self.aggregate_type = OptimizationAggregatorKind.str_to_enum_value(
                self.aggregate_type
            )

        if isinstance(self.effects, str):
            self.effects = OptimizationEffectsKind.str_to_enum_value(self.effects)


@dataclass
class OptimizerModel(PricingModel):
    """Dataclass assembling all optimization parameters.

    Args:
      schedule (List[OptimizerSchedule]): Schedule instance
      selector (OptimizerSelector): Selector instance
      operator (OptimizerOperator): Operator instance
      other (Optional[Mapping[str, Any]]): Other fields (for backwards compatibility)
    """

    schedule: List[OptimizerSchedule]
    selector: OptimizerSelector
    operator: OptimizerOperator
    other: Mapping[str, Any] = None

    def __post_init__(self):

        self.schedule = sorted(
            self.schedule, key=lambda sch: sch.from_dbd, reverse=True
        )

        if not isinstance(self.selector, OptimizerSelector):
            raise TypeError(f"Unexpected type for selector: {type(self.selector)}")

        if not isinstance(self.operator, OptimizerOperator):
            raise TypeError(f"Unexpected type for operator: {type(self.operator)}")

        if self.other is None:
            self.other = dict()


def make_pricing_optimizer_from_json(
    filename_or_dict: Union[str, dict]
) -> OptimizerModel:
    """Make a pricing optimizer instance from a json representation (from file or dict).

    Args:
        filename_or_dict (Union[str, dict]): JSON filename or dictionary in json format

    Examples from file:
    ``my_pricing_optimizer.json``
    ```json
    {
      "schedule": {
        "INF": 7,
        "7": 2
      },
      "selector": {
        "since": "2 years",
        "filters": []
      },
      "operator": {
        "forecaster": "q-forecast",
        "aggregate": "exponential 1.5",
        "optimizer": {
          "type": "qsd",
          "max_requests_per_day": 50,
          "price_points": 30,
          "ebc_samples": 5
        },
        "effects": "none"
      }
    }
    ```

    ```py
    my_pricing_optimizer = make_pricing_optimizer_from_json("my_pricing_optimizer.json")
    ```
    """

    model_id, filename, md5hash, content = parse_data_from_json(filename_or_dict)

    if not isinstance(content, dict):
        raise TypeError(f"Expected dict format in {filename_or_dict}")

    content: dict

    mandatory_keys = ["schedule", "selector", "operator"]
    if not all([k in content for k in mandatory_keys]):
        raise ValueError(
            f"Not all mandatory keys present in content. Requred: {mandatory_keys}"
        )

    # ---- Set schedule
    schedule_list = [
        OptimizerSchedule(from_dbd=since, day_frequency=freq)
        for since, freq in content["schedule"].items()
    ]

    # ---- Set selector
    qty, unit = content["selector"]["since"].split(" ")
    filters = content["selector"]["filters"]
    selector = OptimizerSelector(since_qty=qty, since_unit=unit, filters=filters)

    agg_field = content["operator"]["aggregate"]
    if " " in agg_field:
        agg_type, agg_value = agg_field.split(" ")
    else:
        agg_type = agg_field
        agg_value = None

    # ---- Set maximizer
    maximizer_type = content["operator"]["optimizer"]["type"]
    maximizer = None
    if maximizer_type == "qsd":
        maximizer = DPQSDMaximizer(
            max_requests_per_day=content["operator"]["optimizer"][
                "max_requests_per_day"
            ],
            price_points=content["operator"]["optimizer"]["price_points"],
            ebc_samples=content["operator"]["optimizer"]["ebc_samples"],
        )
    else:
        raise ValueError(f"Unknown maximizer type {maximizer_type}")

    other = {ok: ov for ok, ov in content.items() if ok not in mandatory_keys}

    # ---- Set operator
    operator = OptimizerOperator(
        forecaster_type=content["operator"]["forecaster"],
        aggregate_type=agg_type,
        aggregate_value=agg_value,
        maximizer=maximizer,
        effects=content["operator"]["effects"],
    )

    return OptimizerModel(
        id=model_id,
        filename=filename,
        cnt=json.dumps(content),
        hash=md5hash,
        kind=PricingModelKind.OPTIMIZER,
        extension=FileExtensions.JSON,
        schedule=schedule_list,
        selector=selector,
        operator=operator,
        other=other,
    )
