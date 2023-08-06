from typing import List, Optional, Union
from rmlab._api.upload import APIUploadInternal
from rmlab.data.items import (
    Flight,
)
from rmlab._util import run_async_tasks
from rmlab.data.flight import (
    FlightDataBooks,
    FlightDataPricePerSeatSettings,
    FlightDataThresholdSettings,
)


class APIUploadFlightData(APIUploadInternal):
    """Interface to upload flight data to server"""

    async def upload_flights(
        self,
        scen_id: int,
        data_fn: str,
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> None:
        """Upload a set of flights defined in a file.

        Args:
            scen_id (int): Scenario ID
            data_fn (str): Filename (.csv or .json) defining the flights
            citysector_id (Optional[str], optional): A citysector ID if all flights belong to the same citysector. Defaults to None.
            sector_id (Optional[str], optional): A sector ID if all flights belong to the same sector. Defaults to None.

        Arguments `citysector_id` and `sector_id` are always optional. If any of them provided, concurrent uploads of flights
            files belonging to different citysectors/sectors are allowed.

        Where `data_fn` can refer to:
        * a **CSV file**, for instance:
        ```csv
        Airline,Aircraft,Origin,Destination,Flight number,On sale date,Departure date,Departure time,Duration
        MyCarrier,Airbus A320-b,MAD,GVA,2277,2022-04-01,2022-05-15,T16:30,T02:00
        MyCarrier,Airbus A320-b,MAD,GVA,2277,2022-04-01,2022-05-17,T20:30,T02:00
        ```

        * a **JSON file**, for instance:
        ```json
        [
            {"airline": "MyCarrier", "aircraft": "Airbus A320-b", "origin": "MAD", "destination": "GVA", "flight_number": "2277", "on_sale_date": "2022-04-01", "departure_date": "2022-05-15", "departure_time": "T16:30", "duration": "T02:00", },
            {"airline": "MyCarrier", "aircraft": "Airbus A320-b", "origin": "MAD", "destination": "GVA", "flight_number": "2277", "on_sale_date": "2022-04-01", "departure_date": "2022-05-17", "departure_time": "T20:30", "duration": "T02:00", },
        ]
        ```
        """

        await self._upload_unbounded_items(
            scen_id, Flight, data_fn, citysector_id=citysector_id, sector_id=sector_id
        )

    async def upload_flights_data(
        self,
        scen_id: int,
        flights_data: List[
            Union[
                FlightDataBooks,
                FlightDataThresholdSettings,
                FlightDataPricePerSeatSettings,
            ]
        ],
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> None:
        """Upload flight data of multiple flights belonging to a citysector or sector to server.

        Any previous existing data is overwritten.
        At least `citysector_id` and/or `sector_id` associated to the flights must be defined.

        Args:
            scen_id (int): Scenario ID
            flights_data (List[Union[FlightDataBooks, FlightDataThresholdSettings, FlightDataPricePerSeatSettings]]): List of flights data to upload.
            citysector_id (Optional[str], optional): Target citysector ID. Defaults to None.
            sector_id (Optional[str], optional): Target sector ID. Defaults to None.

        Raises:
            ValueError: If none of `citysector_id`, `sector_id` is defined
            ValueError: If one of flight data list elements has incorrect type.
            MultipleError: If several of flight data list elements have incorrect types.
        """

        if citysector_id is None and sector_id is None:
            raise ValueError(
                f"Require definition of either `citysector_id` or `sector_id`"
            )

        endpoint_limit = self._api_endpoints_limits.data_flight_post

        if len(flights_data) > endpoint_limit:

            # Sequentially upload data in chunks to keep the request payloads and server load controlled

            for chunk_start in range(0, len(flights_data), endpoint_limit):

                chunk_end = chunk_start + endpoint_limit
                if chunk_end > len(flights_data):
                    chunk_end = -1

                await run_async_tasks(
                    [
                        self._upload_flight_data(
                            scen_id,
                            flight_data,
                            citysector_id=citysector_id,
                            sector_id=sector_id,
                        )
                        for flight_data in flights_data[chunk_start:chunk_end]
                    ],
                    return_results=False,
                )

        else:

            await run_async_tasks(
                [
                    self._upload_flight_data(
                        scen_id,
                        flight_data,
                        citysector_id=citysector_id,
                        sector_id=sector_id,
                    )
                    for flight_data in flights_data
                ],
                return_results=False,
            )
