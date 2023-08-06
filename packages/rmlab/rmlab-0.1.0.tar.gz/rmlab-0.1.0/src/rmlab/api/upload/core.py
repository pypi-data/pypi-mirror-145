"""Interface for core data uploading. """

import os
from typing import Optional
from rmlab._api.upload import APIUploadInternal
from rmlab.data.items import (
    Aircraft,
    Airline,
    Airport,
    City,
    Country,
    Schedule,
)


class APIUploadCore(APIUploadInternal):
    """Exposes functions for uploading local data to the server."""

    async def upload_aircrafts(self, scen_id: int, data_fn: str) -> None:
        """Upload a set of aircrafts defined in a file.


        Args:
            scen_id (int): Scenario ID
            data_fn (str): Filename `.csv` or `.json` defining the aircrafts

        Where `data_fn` can refer to:

        * a **CSV file**, for instance:
        ```csv
        Model,Seat capacity
        Airbus A320-a,174
        Airbus A320-b,180
        ```

        * a **JSON file**, for instance:
        ```json
        [
            {"model": "Airbus A320-a", "seat_capacity": 174},
            {"model": "Airbus A320-b", "seat_capacity": 180},
        ]
        ```

        Raises:
            ValueError: If file extension is invalid
            FileNotFoundError: If file does not exist
        """

        await self._upload_bounded_items(
            scen_id=scen_id, category=Aircraft, data_fn=data_fn
        )

    async def upload_airlines(self, scen_id: int, data_fn: str) -> None:
        """Upload a set of airlines defined in a file.

        Args:
            scen_id (int): Scenario ID
            data_fn (str): Filename `.csv` or `.json` defining the airlines

        Where `data_fn` can refer to:

        * a **CSV file**, for instance:
        ```csv
        Name,Type
        MyCarrier,low-cost
        AnotherCarrier,low-cost
        MyLegacyCarrier,legacy
        ```

        * a **JSON file**, for instance:
        ```json
        [
            {"name": "MyCarrier", "type": "low-cost"},
            {"name": "AnotherCarrier", "type": "low-cost"},
            {"name": "MyLegacyCarrier", "type": "legacy"},
        ]
        ```

        Raises:
            ValueError: If file extension is invalid
            FileNotFoundError: If file does not exist
        """

        await self._upload_bounded_items(
            scen_id=scen_id, category=Airline, data_fn=data_fn
        )

    async def upload_airports(self, scen_id: int, data_fn: str) -> None:
        """Upload a set of airports defined in a file.

        Args:
            scen_id (int): Scenario ID
            data_fn (str): Filename `.csv` or `.json` defining the airports

        Where `data_fn` can refer to:

        * a **CSV file**, for instance:
        ```csv
        Name,City,Altitude,Latitude,Longitude,ICAO,IATA
        Geneva,Geneva,431,46.238,6.109,LSGG,GVA
        Madrid,Madrid,619,40.294,-3.724,LEMD,MAD
        London Gatwick,London,60,51.148,-0.19,EGKK,LGW
        London Heathrow,London,25,51.477,-0.461,EGLL,LHR
        ```

        * a **JSON file**, for instance:
        ```json
        [
            {"name": "Geneva", "city": "Geneva", "altitude": 431, "latitude": 46.238, "longitude": 6.109, "icao": "LSGG", "iata": "GVA"},
            {"name": "Madrid", "city": "Madrid", "altitude": 619, "latitude": 40.294, "longitude": -3.724, "icao": "LEMD", "iata": "MAD"},
            {"name": "London Gatwick", "city": "London", "altitude": 60, "latitude": 51.148, "longitude": -0.19, "icao": "EGKK", "iata": "LGW"},
            {"name": "London Heathrow", "city": "London", "altitude": 25, "latitude": 51.477, "longitude": -0.461, "icao": "EGLL", "iata": "LHR"},
        ]
        ```

        * **NOTE**: Airport *cities* must reference previously uploaded ``City`` items with the same `City.name`.

        Raises:
            ValueError: If file extension is invalid
            FileNotFoundError: If file does not exist
            rmlab_errors.ClientError: If any of the referenced cities does not exist in server
        """

        await self._upload_bounded_items(
            scen_id=scen_id, category=Airport, data_fn=data_fn
        )

    async def upload_cities(self, scen_id: int, data_fn: str) -> None:
        """Upload a set of cities defined in a file.

        Args:
            scen_id (int): Scenario ID
            data_fn (str): Filename `.csv` or `.json` defining the cities

        Where ``data_fn`` can refer to:

        * a **CSV file**, for instance:
        ```csv
        Name,Country
        Geneva,Swizterland
        Madrid,Spain
        London,United Kingdom
        ```

        * a **JSON file**, for instance:
        ```json
        [
            {"name": "Geneva", "country": "Switzerland"},
            {"name": "Madrid", "country": "Spain"},
            {"name": "London", "country": "United Kingdom"},
        ]
        ```

        * **NOTE**: City *countries* must reference previously uploaded ``Country`` items with the same `Country.name`.

        Raises:
            ValueError: If file extension is invalid
            FileNotFoundError: If file does not exist
            rmlab_errors.ClientError: If any of the referenced countries does not exist in server
        """

        await self._upload_bounded_items(
            scen_id=scen_id, category=City, data_fn=data_fn
        )

    async def upload_countries(self, scen_id: int, data_fn: str) -> None:
        """Upload a set of countries defined in a file.

        Args:
            scen_id (int): Scenario ID
            data_fn (str): Filename `.csv` or `.json` defining the countries

        Where `data_fn` can refer to:

        * a **CSV file**, for instance:
        ```csv
        Name,Currency
        Swizterland,chf
        Spain,eur
        United Kingdom,gbp
        ```

        * a **JSON file**, for instance:
        ```json
        [
            {"name": "Switzerland", "currency": "chf"},
            {"name": "Spain", "currency": "eur"},
            {"name": "United Kingdom", "currency": "gbp"},
        ]
        ```

        Raises:
            ValueError: If file extension is invalid
            FileNotFoundError: If file does not exist
        """

        await self._upload_bounded_items(
            scen_id=scen_id, category=Country, data_fn=data_fn
        )

    async def upload_schedules(
        self,
        scen_id: int,
        data_fn: str,
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ) -> None:
        """Upload a set of flights schedules defined in a file.

        Args:
            scen_id (int): Scenario ID
            data_fn (str): Filename `.csv` or `.json` defining the schedules
            citysector_id (Optional[str], optional): A citysector ID if all schedules belong to the same citysector. Defaults to None.
            sector_id (Optional[str], optional): A sector ID if all schedules belong to the same sector. Defaults to None.

        Arguments `citysector_id` and `sector_id` are always optional. If provided, concurrent uploads of schedules
            files belonging to different citysectors/sectors are allowed.

        Where `data_fn` can refer to:

        * a **CSV file**, for instance:
        ```csv
        Airline,Aircraft,Origin,Destination,Days of Week,Departure time,Duration,Flight number,Sell before days,From Date,To Date
        MyCarrier,Airbus A320-b,MAD,GVA,-2-4-6-,T08:00,T02:00,2277,15,2022-04-01,2022-05-31
        MyCarrier,Airbus A320-a,MAD,GVA,1-3-5-7,T16:00,T02:00,2278,15,2022-04-01,2022-05-31
        MyCarrier,Airbus A320-b,GVA,MAD,-2-4-6-,T10:30,T01:30,2377,15,2022-04-01,2022-05-31
        MyCarrier,Airbus A320-a,GVA,MAD,1-3-5-7,T18:30,T01:30,2378,15,2022-04-01,2022-05-31
        ```

        * a **JSON file**, for instance:
        ```json
        [
            {"airline": "MyCarrier", "aircraft": "Airbus A320-b", "origin": "MAD", "destination": "GVA", "days_of_week": "-2-4-6-", "departure_time": "T08:00", "duration": "T02:00", "flight_number": "2277", "sell_before_days": 45, "from_date": "2022-04-01", "to_date": "2022-05-31"},
            {"airline": "MyCarrier", "aircraft": "Airbus A320-b", "origin": "MAD", "destination": "GVA", "days_of_week": "1-3-5-7", "departure_time": "T16:00", "duration": "T02:00", "flight_number": "2278", "sell_before_days": 45, "from_date": "2022-04-01", "to_date": "2022-05-31"},
            {"airline": "MyCarrier", "aircraft": "Airbus A320-b", "origin": "GVA", "destination": "MAD", "days_of_week": "-2-4-6-", "departure_time": "T10:30", "duration": "T01:30", "flight_number": "2377", "sell_before_days": 45, "from_date": "2022-04-01", "to_date": "2022-05-31"},
            {"airline": "MyCarrier", "aircraft": "Airbus A320-b", "origin": "GVA", "destination": "MAD", "days_of_week": "1-3-5-7", "departure_time": "T10:30", "duration": "T01:30", "flight_number": "2378", "sell_before_days": 45, "from_date": "2022-04-01", "to_date": "2022-05-31"},
        ]
        ```

        * **NOTE**: Schedule *airlines* must reference previously uploaded ``Airline`` items with the same `Airline.name`.
        * **NOTE**: Schedule *aircrafts* must reference previously uploaded ``Aircraft`` items with the same `Aircraft.model`.
        * **NOTE**: Schedule *origins* must reference previously uploaded ``Airport`` items with the same `Airport.iata`.
        * **NOTE**: Schedule *destinations* must reference previously uploaded ``Airport`` items with the same `Airport.iata`.
        * **NOTE**: No two schedules with overlapping date ranges (*from_date*, *to_date*), and overlapping days of week, with the same *flight_number* are allowed.


        Raises:
            ValueError: If file extension is invalid
            FileNotFoundError: If file does not exist
            rmlab_errors.ClientError: If any of the previous Notes are not satisfied
        """

        await self._upload_unbounded_items(
            scen_id,
            Schedule,
            data_fn,
            citysector_id=citysector_id,
            sector_id=sector_id,
        )

    async def upload_batch_core(
        self,
        scen_id: int,
        *,
        aircraft_items_fn: Optional[str] = None,
        airline_items_fn: Optional[str] = None,
        airport_items_fn: Optional[str] = None,
        city_items_fn: Optional[str] = None,
        country_items_fn: Optional[str] = None,
        schedule_items_fn: Optional[str] = None,
    ):
        """Upload a set of items defined in files to server.

        Args:
            scen_id (int): Scenario ID
            aircraft_items_fn (Optional[str], optional): File name with aircraft items. Defaults to None.
            airline_items_fn (Optional[str], optional): File name with airline items. Defaults to None.
            airport_items_fn (Optional[str], optional): File name with airport items. Defaults to None.
            city_items_fn (Optional[str], optional): File name with city items. Defaults to None.
            country_items_fn (Optional[str], optional): File name with country items. Defaults to None.
            schedule_items_fn (Optional[str], optional): File name with flights schedule items. Defaults to None.

        Raises:
            FileNotFoundError: If any of the files does not exist
        """

        not_existing_fns = [
            fn
            for fn in [
                airport_items_fn,
                airline_items_fn,
                airport_items_fn,
                city_items_fn,
                country_items_fn,
                schedule_items_fn,
            ]
            if fn and not os.path.exists(fn)
        ]

        if len(not_existing_fns) > 0:
            raise FileNotFoundError(not_existing_fns)

        if airline_items_fn:
            await self._upload_bounded_items(scen_id, Airline, data_fn=airline_items_fn)

        if aircraft_items_fn:
            await self._upload_bounded_items(
                scen_id, Aircraft, data_fn=aircraft_items_fn
            )

        if country_items_fn:
            await self._upload_bounded_items(scen_id, Country, data_fn=country_items_fn)

        if city_items_fn:
            await self._upload_bounded_items(scen_id, City, data_fn=city_items_fn)

        if airport_items_fn:
            await self._upload_bounded_items(scen_id, Airport, data_fn=airport_items_fn)

        if schedule_items_fn:
            await self._upload_unbounded_items(
                scen_id, Schedule, data_fn=schedule_items_fn
            )
