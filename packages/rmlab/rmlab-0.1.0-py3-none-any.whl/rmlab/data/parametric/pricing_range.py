"""A pricing range defines the amount of fare prices, the min-max range of prices, and the fare identifications."""

from dataclasses import dataclass
import json
from typing import List, Union
from rmlab._data.conversions import parse_data_from_json
from rmlab._data.enums import FileExtensions, PricingModelKind
from rmlab.data.parametric._pricing_base import PricingModel


@dataclass
class RangeModel(PricingModel):
    """Dataclass for pricing range parameters.Parameters specifying .

    Args:
        granularity (int): Number of fares
        min_fare (int): Price per seat of the lowest fare
        max_fare (int): Price per seat of the highest fare
        tags (List[str]): List of single-character identifiers for all fares. Defaults

    Example
    ```py
    range = RangeModel(granularity=4, min_fare=40, max_fare=200, tags=["D", "C", "B", "A"])
    ```

    """

    granularity: int
    min_fare: float
    max_fare: float
    tags: List[str]

    def __post_init__(self):

        if len(self.tags) != self.granularity:
            raise ValueError(
                f"Number of tag identifiers `{len(self.tags)}` must match granularity `{self.granularity}`"
            )


def make_pricing_range_from_json(filename_or_dict: Union[str, dict]) -> RangeModel:
    """Make a pricing range instance from a json representation (from file or dict).

    Args:
        filename_or_dict (Union[str, dict]): JSON filename or dictionary in json format

    Examples from dict:
    ```py
    dict_range = {"granularity": 3, "min_fare": 40, "max_fare": 200}
    my_pricing_range = make_from_json(dict_range)
    # Tags will be ["Q", "P", "O"] from lowest to highest price per seat
    ```

    ```py
    dict_range = {"granularity": 3, "min_fare": 40, "max_fare": 200, tags=["C", "B", "A"]}
    my_pricing_range = make_from_json(dict_range)
    ```

    ```py
    dict_range = {"granularity": 3, "min_fare": 40, "max_fare": 200, lowest_tag="Q"}
    my_pricing_range = make_from_json(dict_range)
    # Tags will be ["Q", "P", "O"] from lowest to highest price per seat
    ```

    ```py
    dict_range = {"granularity": 10, "min_fare": 40, "max_fare": 200, highest_tag="A"}
    my_pricing_range = make_from_json(dict_range)
    # Tags will be ["C", "B", "A"] from lowest to highest price per seat
    ```

    Example from file:
    `my_pricing_range.json`
    ```json
    {
      "granularity" : 10,
      "min_fare" : 40,
      "max_fare" : 500,
      "lowest_tag" : "Q"
    }
    ```
    ```py
    my_pricing_range = make_pricing_range_from_json("my_pricing_range.json")
    ```
    """

    model_id, filename, md5hash, content = parse_data_from_json(filename_or_dict)

    if not isinstance(content, dict):
        raise TypeError(f"Expected dict format in {filename_or_dict}")

    content: dict

    tags = None
    if "tags" in content:
        tags = content["tags"]
    elif "lowest_tag" in content:
        lt = content["lowest_tag"]
        if len(lt) != 1:
            raise ValueError(f"`lowest_tag` must be a single character")
        tags = [chr(ord(lt) - t) for t in range(content["granularity"])]
    elif "highest_tag" in content:
        gt = content["highest_tag"]
        if len(gt) != 1:
            raise ValueError(f"`highest_tag` must be a single character")
        tags = [chr(ord(gt) + t) for t in range(content["granularity"])]
    else:
        tags = [chr(ord("Q") - t) for t in range(content["granularity"])]
        # Defaults to ['Q', 'P', 'O', ... if none provided, with 'Q' identifying the lowest fare]

    return RangeModel(
        id=model_id,
        filename=filename,
        cnt=json.dumps(content),
        hash=md5hash,
        kind=PricingModelKind.RANGE,
        extension=FileExtensions.JSON,
        granularity=int(content["granularity"]),
        min_fare=float(content["min_fare"]),
        max_fare=float(content["max_fare"]),
        tags=list(tags),
    )
