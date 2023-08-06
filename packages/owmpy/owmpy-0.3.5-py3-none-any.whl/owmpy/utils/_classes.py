import aiohttp as _aiohttp


Number = int | float


class _AutomaticClient:
    client: _aiohttp.ClientSession
    appid: str | None

    def __init__(self, client: _aiohttp.ClientSession | None = None, appid: str | None = None) -> None:
        self.client = client or _aiohttp.ClientSession()
        self.appid = appid or None

    async def __aenter__(self, *args):
        return self

    async def __aexit__(self, *args):
        await self.client.close()
        return self
