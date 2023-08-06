# Open Weather Mappy

Wrapper to interact with the [Open Weather Map](https://openweathermap.org/api) Current Weather Data API. Install from pip under the name `owmpy`.

## Usage

Import the class and make requests.

```py
import asyncio
from os import getenv

from owmpy.current import CurrentWeather


async def main():
    # Get a weather token from openweathermap.org
    async with CurrentWeather(appid=getenv("WEATHER_TOKEN")) as weather:
        response = await weather.get((0, 0))
        print(response)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
```

Optionally, you can supply your own ClientSession:

```py
import aiohttp
weather = CurrentWeather(appid="token", client=aiohttp.ClientSession())
```
