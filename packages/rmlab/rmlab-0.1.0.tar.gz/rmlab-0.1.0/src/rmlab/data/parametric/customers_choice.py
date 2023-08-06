"""A choice model emulates customers selection criteria while choosing flight booking offers.
From a functional perspective, a choice model maps 
a list of booking offers for a given flight to a selected booking offer, 
either deterministically or by sampling from some statistical distribution. 
The selected offer may be none (ie, all offers are rejected), with some probability depending on the type of the model.

Args:
  class_name (str): Identifier of a customers class (eg `business`, `leisure`)
"""

from dataclasses import dataclass
import json
from typing import List, Union
from rmlab._data.conversions import parse_data_from_json
from rmlab._data.enums import CustomersModelKind, FileExtensions

from rmlab.data.parametric._customers_base import CustomersModel


@dataclass
class BaseChoiceModel(CustomersModel):
    """Base dataclass for choice models."""


@dataclass
class Random(BaseChoiceModel):
    """Parameterless model. Picks a single booking offer randomly regardless of any parameter.
    The probability of choosing none is zero.

    Args:
      class_name (str): Customers class

    """

    class_name: str


@dataclass
class Cheapest(BaseChoiceModel):
    """Parameterless model. Picks the booking offer with the minimum price.
    Randomly breaking ties if two offers have the same minimum price.
    The probability of choosing none is zero.

    Args:
      class_name (str): Customers class

    """

    class_name: str


# @dataclass
# class MNLSingleReject(BaseChoiceModel):
#   """
#   A multinomial logistic model is used to score the list of booking offers
#   according to its price.
#
#   Requires a beta parameter that quantifies the sensitivity to price, required to define a function
#   that returns a score
#   $$
#     s = \exp(-p/ \\beta)
#   $$
#
#   in [0,1] for a given positive price per seat *p* of each booking offer. The lesser the price,
#   the closer the score is to 1. The greater the *beta*, the less sensitive to price are the customers.
#
#   When there are more than one booking offers, all the scores of the booking offers
#   are normalized to get a discrete distribution over them. Then this distribution
#   is sampled to pick the winner offer.
#
#   If there is a single booking offer, then there is a single score *s < 1*. In this case,
#   there is a non-zero probability of rejecting this single offer *(s - 1)*.
#
#   This model will cause an inelastic demand when there are several flights competing, since the existence of more than 1 booking offer makes the rejection probability 0, so the customers will absorb all the demand.
#   Thus this model is more realistic when there are no competitors.
#
#   Args:
#     class_name (str): Name identifier of the customers class
#     beta (float): $$\\beta$$
#
#   Example:
#   ```py
#   bus_req_model = MNLSingleReject(class_name="business", beta=140)
#   leis_req_model = MNLSingleReject(class_name="leisure", beta=60)
#   ```
#
#   Naming:
#
#   * *MNL*: MultiNomial Logistic
#
#   * *Single reject*: There is a *rejection* only if there is a *single* offer
#   """
#
#   class_name: str
#   beta: float


@dataclass
class Multinomial(BaseChoiceModel):
    """
    A multinomial logistic model is used to score the list of booking offers according to its price.

    This model specifies a price sensitivity parameter $\\beta$ and a rejection probability
    parameter $prob_{reject}$ in [0, 1], so that the probability of rejecting all offers is always fixed to $prob_{reject}$.

    The probability of accepting any booking offer is thus $1 - prob_{reject}$, and the
    acceptance probabilities of the offers given no-rejection are weighted according to a score *s*
    computed from their prices *p*:
    $$
      s = \exp(-p/ \\beta).
    $$

    Note that regarding $\\beta$ sensitivity, its magnitude corresponds to the *unit*
    currency (eg: *euros*, *gbps*, ..., and **not** *euro cents* or *gbp pennies*, ...).

    Args:
      class_name (str): Customers class
      beta (float): $$\\beta$$
      reject_prob (float): $prob_{reject}$

    """

    class_name: str
    beta: float
    reject_prob: float

    def __post_init__(self):

        if self.beta <= 0:
            raise ValueError(f"Beta must be positive, got `{self.beta}`")

        if self.reject_prob < 0 or self.reject_prob >= 1:
            raise ValueError(f"Reject probability must be in [0, 1)")


@dataclass
class MultipleChoiceModels(BaseChoiceModel):
    """An aggregation of request models for different customer classes.

    Example:
    ```py
    bus_choice_model = Multinomial(class_name="business", beta=30, reject_prob=0.5
    lei_choice_model = Cheapest(class_name="leisure", beta=10)
    rnd_choice_model = Random(class_name="careless")

    mul_chouce_model = MultipleChoiceModels(bus_choice_model, lei_choice_model, rnd_choice_model)
    ```

    JSON representation:
    ```json
    {
      "business" : {"type" : "mnl_multiple_reject","beta": 140.0, "reject_prob": 0.5},
      "leisure": {"type": "cheapest"},
      "careless": {"type": "random"}
    }
    ```
    """

    models: List[BaseChoiceModel]


def make_customers_choice_model_from_json(
    filename_or_dict: Union[str, dict]
) -> BaseChoiceModel:
    """Make a request model instance from a json representation (from file or dict).

    Args:
        filename_or_dict (Union[str, dict]): JSON filename or dictionary in json format

    Raises:
        ValueError: If JSON is not a dict
        ValueError: If model type is invalid
        ValueError: If JSON content is empty

    Returns:
        A customers request model instance


    Example from dict:
    ```py
    my_dict = dict()
    my_dict["business"] = {"type": "poisson", "beta": 30.0, "scale": 400, "lambda_seats": 1.5}
    my_dict["leisure"] = {"type": "poisson", "beta": 10.0, "scale": 300, "lambda_seats": 3}

    my_choice_model = make_from_json(my_dict)
    ```

    Example from file:
    `my_choice_model.json`
    ```json
    {
      "business" : {"type" : "mnl_multiple_reject","beta": 140.0, "reject_prob": 0.5},
      "leisure": {"type": "cheapest"},
      "careless": {"type": "random"}
    }
    ```
    ```py
    my_choice_model = make_customers_choice_model_from_json("my_choice_model.json")
    ```
    """

    model_id, filename, md5hash, content = parse_data_from_json(filename_or_dict)

    if not isinstance(content, dict):
        raise ValueError(f"Expected dict format in {filename_or_dict}")

    content: dict

    if len(content) > 0:
        models = list()
        for class_name, fields in content.items():
            if fields["type"] == "random":
                models.append(
                    Random(
                        id=model_id,
                        filename=filename,
                        cnt=json.dumps(content),
                        hash=md5hash,
                        kind=CustomersModelKind.CHOICE,
                        extension=FileExtensions.JSON,
                        class_name=class_name,
                    )
                )
            elif fields["type"] == "cheapest":
                models.append(
                    Cheapest(
                        id=model_id,
                        filename=filename,
                        cnt=json.dumps(content),
                        hash=md5hash,
                        kind=CustomersModelKind.CHOICE,
                        extension=FileExtensions.JSON,
                        class_name=class_name,
                    )
                )
            elif fields["type"] == "mnl_multiple_reject":
                models.append(
                    Multinomial(
                        id=model_id,
                        filename=filename,
                        cnt=json.dumps(content),
                        hash=md5hash,
                        kind=CustomersModelKind.CHOICE,
                        extension=FileExtensions.JSON,
                        class_name=class_name,
                        beta=float(fields["beta"]),
                        reject_prob=float(fields["reject_prob"]),
                    )
                )
            else:
                raise ValueError(f'Unknown request model type {fields["type"]}')

        if len(models) > 1:
            return MultipleChoiceModels(
                id=model_id,
                filename=filename,
                cnt=json.dumps(content),
                hash=md5hash,
                kind=CustomersModelKind.REQUEST,
                extension=FileExtensions.JSON,
                models=models,
            )
        else:
            return models[0]

    else:
        raise ValueError(f"Empty content")
