"""
Parametric filters assign parametric models to data items.
"""

from hashlib import md5
import json
from typing import List, Union
from dataclasses import dataclass

from rmlab._data.conversions import parse_data_from_json
from rmlab._data.enums import ParametricFilterClassKind
from rmlab.data.items import PModel
from rmlab._data.types import (
    BoundedItem,
    CoreItem,
)


@dataclass
class PFilter(CoreItem, BoundedItem):
    """
    Construct parametric models to items associations.

    Args:
        filter_class (str): Specifies the fields of the target item that are inspected upon filtering matching.
        filter_content (str): The content to be matched
        pmodel_id (str): A pointer (identifier) to the model which stores the set of parameters that we want to assign

    Following examples explain how to associate pmodels to markets and flights.
    In these cases, there is a hierachy that is obeyed when multiple models match multiple
    filtering criteria for a given category item.

    Examples:

    ## Assigning customers models to *citysectors* and *cityroutes*

    Customers models can be assigned either to:

    * **citysectors**: A city pair with defined directionality (eg: a *CitySector* with ID CityA->CityB).

    * **cityroutes**: A city pair with undefined directionality (eg: a *CityRoute* with ID CityA<>CityB).

    Following examples show different filters to associate a given `my_customers_model.json` to:

    **All citysectors:**
    ```py
    pf = ParametricFilter(
        filter_class="network",
        filter_content="",
        pmodel_id="my_customers_model.json")
    ```

    **A cityroute with ID `CityA<>CityB`:**
    ```py
    pf = ParametricFilter(
        filter_class="network",
        filter_content="CityA<>CityB",
        pmodel_id="my_customers_model.json")
    ```

    ## Assigning pricing models models to *flights*

    First, note that:

    * A schedule represents a set of flights departing within a date period,
    referring to a given airline and sector.

    * A sector represents a pair of airports with defined directionality
    (AirportA-> AirportB). We use IATA coding to identify them (eg AAABBB)

    * A route represents a pair of airports with undefined directionality (AirportA <> AirportB).
    We use <>-separated IATA coding to identify them (eg AAA<>BBB)

    Following examples show how to create parametric filters to associate a given `my_pricing_model.json` to:

    **All flights of all schedules:**

    ```py
    pf = ParametricFilter(
        filter_class="network",
        filter_content="",
        pmodel_id="my_pricing_model.json")
    ```

    **All flights of cityroute `CityA<>CityB`:**

    ```py
    pf = ParametricFilter(
        filter_class="cityroute",
        filter_content="CityA<>CityB",
        pmodel_id="my_pricing_model.json")
    ```

    **All flights of citysector `CityA->CityB`:**

    ```py
    pf = ParametricFilter(
        filter_class="cityroute",
        filter_content="CityA->CityB",
        pmodel_id="my_pricing_model.json")
    ```

    **All flights of route `AAA<>BBB`:**

    ```py
    pf = ParametricFilter(
        filter_class="route",
        filter_content="AAA<>BBB",
        pmodel_id="my_pricing_model.json")
    ```

    **All flights of sector `AAABBB`:**

    ```py
    pf = ParametricFilter(
        filter_class="sector",
        filter_content="AAABBB",
        pmodel_id="my_pricing_model.json")
    ```

    **All flights of airline `MyAirline`:**

    ```py
    pf = ParametricFilter(
        filter_class="airline",
        filter_content="MyAirline",
        pmodel_id="my_pricing_model.json")
    ```

    **All flights with flight number `2744`:**

    ```py
    pf = ParametricFilter(
        filter_class="flight_number",
        filter_content="2744",
        pmodel_id="my_pricing_model.json")
    ```

    **All flights whose departure dates are fully contained within a given period `2022/05/24-2022/12/31`:**

    ```py
    pf = ParametricFilter(
        filter_class="in_period",
        filter_content="20220524-20221231",
        pmodel_id="my_pricing_model.json")
    ```

    **All flights sharing several attributes:**

    * whose departure dates are fully contained within a given period `2022/05/24-2022/12/31`
    * belonging to an airline `MyAirline`
    * covering citysector `CityA->CityB`

    ```py
    pf = ParametricFilter(
        filter_class=["in_period", "airline", "citysector"],
        filter_content=["20220524-20221231", "MyAirline", "CityA->CityB"],
        pmodel_id="my_pricing_model.json")
    ```

    All previous examples work as json representations too:
    ```json
    {
      "filter_class": "String",
      "filter_content": "String",
      "pmodel_id": "String"
    }
    ```
    """

    filter_class: List[ParametricFilterClassKind]
    filter_content: List[str]
    pmodel_id: str

    def __post_init__(self):

        if isinstance(self.filter_class, str):
            self.filter_class = [self.filter_class]

        if isinstance(self.filter_content, str):
            self.filter_content = [self.filter_content]

        for i, fc in enumerate(self.filter_class):
            if isinstance(fc, str):
                self.filter_class[i] = ParametricFilterClassKind.str_to_enum_value(fc)

        if len(self.filter_class) != len(self.filter_content):
            raise ValueError(
                f"Mismatch in number of elements of `filter_class` and `filter_content`: `{self.filter_class}`, `{self.filter_content}`"
            )


def make_parametric_filters_from_json(filename_or_list: Union[str, list]) -> PModel:
    """Make a parametric filter instance from a json representation (from file or list).

    Args:
        filename_or_list (Union[str, list]): JSON filename or list of dictionaries in json format

    Example from file:
    `my_parametric_filters.json`
    ```json
    [
      {
        "filter_class": "network",
        "filter_content": "",
        "pmodel_id": "pricing_range.sample.json"
      },
      {
        "filter_class": "in_period",
        "filter_content": "20220524-20221231",
        "pmodel_id": "pricing_behavior.sample.json"
      },
      {
        "filter_class": "airline",
        "filter_content": "MyAirline",
        "pmodel_id": "pricing_optimizer.sample.json"
      },
      {
        "filter_class": "citysector",
        "filter_content": "CityA->CityB",
        "pmodel_id": "customers_request.poisson_bl1.json"
      },
      {
        "filter_class": "sector",
        "filter_content": "CCCDDD",
        "pmodel_id": "customers_choice.mnl_bl1.json"
      }
    ]
    ```

    ```py
    my_filters = make_parametric_filters_from_json("my_parametric_filters.json")
    ```

    """

    model_id, filename, md5hash, content = parse_data_from_json(filename_or_list)

    if not isinstance(content, list):
        raise ValueError(f"Expected list format in {filename_or_list}")

    content: list

    if len(content) > 0:

        # Used for json validation only, for the moment

        models = list()

        for fields in content:

            filter_class = fields["filter_class"]
            filter_content = fields["filter_content"]

            if isinstance(filter_class, str) and "&" in filter_class:
                filter_class = filter_class.split("&")

            if isinstance(filter_content, str) and "&" in filter_content:
                filter_content = filter_content.split("&")

            models.append(
                PFilter(
                    id=model_id,
                    filter_class=filter_class,
                    filter_content=filter_content,
                    pmodel_id=fields["pmodel_id"],
                )
            )

        return PModel(
            id=model_id, filename=filename, hash=md5hash, content=json.dumps(content)
        )

    else:
        raise ValueError(f"Empty content")
