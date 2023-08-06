"""A request model emulates customers interest on booking flight tickets.
defined by a set of parameters that define the rate of requests per day 
as the departure date approaches and the amount of seats for each request.
"""

from dataclasses import dataclass
import json
from typing import List, Union
from rmlab._data.conversions import parse_data_from_json
from rmlab._data.enums import CustomersModelKind, FileExtensions
from rmlab.data.parametric._customers_base import CustomersModel


@dataclass
class BaseRequestModel(CustomersModel):
    """Base dataclass for request models."""

    pass


@dataclass
class ExponentialPoisson(BaseRequestModel):
    """A particular kind of request model, characterized by an exponential curve that
    for a given day before departure (*d* onwards, from 0 *departure day* to +D *on-sale day*) returns the cumulative booking requests for that day

    $$
    CumulativeRequestsOn(d) = scale · \exp(-d/ \\beta)
    $$

    On a given day before departure *d*, the average booking requests is given by

    $$
    \lambda_{requests}(d) = CumulativeRequestsOn(d) - CumulativeRequestsOn(d+1).
    $$

    Note that $d+1$ is the day *before* $d$.

    From $\lambda_{requests}$ we sample the number of booking requests on day before departure $d$ as:

    $$
    \# booking\,requests(d) \sim Poisson(\lambda_{requests}(d))
    $$

    For each booking request, we also sample the requested seats from a zero-truncated Poisson

    $$
    \# seats\,per\,request \sim Poisson_{ZT}(\lambda_{seats})
    $$

    Args:
      class_name (str): Customers class
      beta (float): $$\\beta$$
      scale (float): $$scale$$
      lambda_seats (float): $$\lambda_{seats}$$

    Examples:
    ```py
    bus_req_model = ExponentialPoisson(class_name="business", beta=30, scale=300, lambda_seats=1.5)
    ```

    JSON representation:
    ```json
    {
      "business": {"type": "poisson", "beta": 30.0, "scale": 400, "lambda_seats": 1.5},
    }
    ```
    """

    class_name: str
    beta: float
    scale: float
    lambda_seats: float


@dataclass
class MultipleRequestModels(BaseRequestModel):
    """An aggregation of request models for different customer classes.

    Example:
    ```py
    bus_req_model = ExponentialPoisson(class_name="business", beta=30, scale=300, lambda_seats=1.5)
    lei_req_model = ExponentialPoisson(class_name="leisure", beta=10, scale=400, lambda_seats=3)

    mul_req_model = MultipleRequestModels(bus_req_model, lei_req_model)
    ```

    JSON representation:
    ```json
    {
      "business": {"type": "poisson", "beta": 30.0, "scale": 400, "lambda_seats": 1.5},
      "leisure": {"type": "poisson", "beta": 10.0, "scale": 300, "lambda_seats": 3}
    }
    ```
    """

    models: List[BaseRequestModel]


def make_customers_request_model_from_json(
    filename_or_dict: Union[str, dict]
) -> BaseRequestModel:
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

    my_req_model = make_from_json(my_dict)
    ```

    Example from file:
    `my_req_model.json`
    ```json
    {
      "business": {"type": "poisson", "beta": 30.0, "scale": 400, "lambda_seats": 1.5},
      "leisure": {"type": "poisson", "beta": 10.0, "scale": 300, "lambda_seats": 3}
    }
    ```
    ```py
    my_req_model = make_customers_request_model_from_json("my_req_model.json")
    ```
    """

    model_id, filename, md5hash, content = parse_data_from_json(filename_or_dict)

    if not isinstance(content, dict):
        raise ValueError(f"Expected dict format in {filename_or_dict}")

    content: dict

    if len(content) > 0:
        models = list()
        for class_name, fields in content.items():
            if fields["type"] == "poisson":
                models.append(
                    ExponentialPoisson(
                        id=model_id,
                        filename=filename,
                        cnt=json.dumps(content),
                        hash=md5hash,
                        kind=CustomersModelKind.REQUEST,
                        extension=FileExtensions.JSON,
                        class_name=class_name,
                        beta=fields["beta"],
                        scale=fields["scale"],
                        lambda_seats=fields["lambda_seats"],
                    )
                )
            else:
                raise ValueError(f'Unknown request model type {fields["type"]}')

        if len(models) > 1:
            return MultipleRequestModels(
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
