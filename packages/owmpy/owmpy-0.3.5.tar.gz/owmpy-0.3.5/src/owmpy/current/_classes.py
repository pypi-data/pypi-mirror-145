from ..utils import Number as _Number
from ..utils import Units, _AutomaticClient
from ._classes import *
from .response import *


class CurrentWeatherAPIException(Exception):
    pass


class CurrentWeather(_AutomaticClient):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    async def get(
        self, coords: tuple[_Number, _Number], units: Units = StandardUnits.STANDARD, lang: str | None = None
    ) -> CurrentWeatherStatus:
        params = {"appid": self.appid, "lat": coords[0], "lon": coords[1], "units": units.api_name}
        if lang:
            params["lang"] = lang

        async with self.client.get(self.BASE_URL, params=params) as resp:
            resp = await resp.json()
            if "cod" in resp and "message" in resp:
                raise CurrentWeatherAPIException(resp["cod"], resp["message"])
            if "rain" in resp:
                keys: set[str] = set(resp["rain"])
                for key in keys:
                    resp["rain"][f"_{key}"] = resp["rain"][key]
                    del resp["rain"][key]

            return CurrentWeatherStatus(**resp)
