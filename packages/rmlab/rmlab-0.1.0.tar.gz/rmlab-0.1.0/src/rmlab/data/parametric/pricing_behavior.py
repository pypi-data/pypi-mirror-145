"""A pricing behavior defines the strategy under which flights assign prices to seats."""

import json
from typing import Union
from dataclasses import dataclass
from rmlab._data.conversions import parse_data_from_json
from rmlab._data.enums import FileExtensions, PricingModelKind
from rmlab.data.parametric._pricing_base import PricingModel


@dataclass
class BaseBehaviorModel(PricingModel):
    """Base class for all types of pricing behavior models."""

    pass


@dataclass
class SeatThresholds(BaseBehaviorModel):
    """A kind of pricing behavior model in which a set of seat thresholds are used to allocate seats to fares based on the flight occupation.

    Args:
      seats_per_dbd (float): Rate of increase in number of seats per day of all thresholds
      zero_shift (float): Per-unit relative displacement of all the thresholds
      squeeze (float): Per-unit relative contraction of the all thresholds

    Example
    ```py
    behavior = SeatThresholds(seats_per_dbd=0.15, zero_shift=0.06, squeeze=0.7)
    ```

    """

    seats_per_dbd: float
    zero_shift: float
    squeeze: float


def make_pricing_behavior_from_json(
    filename_or_dict: Union[str, dict]
) -> BaseBehaviorModel:
    """Make a pricing behavior instance from a json representation (from file or dict).

    Args:
        filename_or_dict (Union[str, dict]): JSON filename or dictionary in json format

    Examples from dict:
    ```py
    dict_behavior = dic()
    dict_behavior["type"] = "rake_straight"
    dict_behavior["seats_per_dbd"] = 0.15
    dict_behavior["zero_shift"] = 0.06
    dict_behavior["squeeze"] = 0.7
    my_pricing_behavior = make_from_json(dict_behavior)
    ```

    Example from file:
    `my_pricing_behavior.json`
    ```json
    {
      "type" : "rake_straight",
      "seats_per_dbd" : 0.15,
      "zero_shift" : 0.06,
      "squeeze" : 0.7
    }
    ```

    ```py
    my_pricing_behavior = make_pricing_behavior_from_json("my_pricing_behavior.json")
    ```

    """

    model_id, filename, md5hash, content = parse_data_from_json(filename_or_dict)

    if not isinstance(content, dict):
        raise TypeError(f"Expected dict format in {filename_or_dict}")

    content: dict

    if content["type"] == "rake_straight":

        return SeatThresholds(
            id=model_id,
            filename=filename,
            cnt=json.dumps(content),
            hash=md5hash,
            kind=PricingModelKind.BEHAVIOR,
            extension=FileExtensions.JSON,
            seats_per_dbd=float(content["seats_per_dbd"]),
            zero_shift=float(content["zero_shift"]),
            squeeze=float(content["squeeze"]),
        )

    else:

        raise ValueError(f'Unknown pricing behavior type `{content["type"]}`')
