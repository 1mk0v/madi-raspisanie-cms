import aiohttp
import pydantic
from .exceptions import (
    NoNetworkConnection,
    RequestedResourceError
)

class HTTPResponse(pydantic.BaseModel):
    status:int
    headers:dict
    body:str | dict
    cookies:dict

class BaseRequests():

    def __init__(self, url:str) -> None:
        self.url = url

    async def _get(self, url) -> HTTPResponse:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url.format(url)) as response:
                    cookies = session.cookie_jar.filter_cookies(self.url) 
                    return HTTPResponse(
                        status=response.status,
                        headers={i:response.headers[i] for i in response.headers},
                        body=await response.text(),
                        cookies={i:cookies[i].coded_value for i in cookies}
                    )
            except aiohttp.client.ServerConnectionError as error:
                raise RequestedResourceError(
                    message=str(error),
                    status_code=500,
                )
            except aiohttp.client.ClientConnectionError as error:
                raise NoNetworkConnection(
                    message=str(error),
                    status_code=500
                )

    async def _post(self, url, data:dict = None) -> HTTPResponse:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=self.url.format(url), data=data) as response:
                    cookies = session.cookie_jar.filter_cookies(self.url) 
                    return HTTPResponse(
                        status=response.status,
                        headers={i:response.headers[i] for i in response.headers},
                        body=await response.text(),
                        cookies={i:cookies[i].coded_value for i in cookies}
                    )
            except aiohttp.client.ServerConnectionError as error:
                raise RequestedResourceError(
                    message=str(error),
                    status_code=500,
                )
            except aiohttp.client.ClientConnectionError as error:
                raise NoNetworkConnection(
                    message=str(error),
                    status_code=500
                )