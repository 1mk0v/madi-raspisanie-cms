import aiohttp
import pydantic
# from .exceptions import BaseRequestsException, NotFoundError

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
            async with session.get(self.url.format(url)) as response:
                cookies = session.cookie_jar.filter_cookies(self.url) 
                return HTTPResponse(
                    status=response.status,
                    headers={i:response.headers[i] for i in response.headers},
                    body=await response.text(),
                    cookies={i:cookies[i].coded_value for i in cookies}
                )


    async def _post(self, url, data:dict = None) -> HTTPResponse:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url.format(url), data=data) as response:
                cookies = session.cookie_jar.filter_cookies(self.url) 
                return HTTPResponse(
                    status=response.status,
                    headers={i:response.headers[i] for i in response.headers},
                    body=await response.text(),
                    cookies={i:cookies[i].coded_value for i in cookies}
                )

    # async def _get_response_or_exception(response:aiohttp.ClientResponse):
    #     if response.status == 404:
    #         raise NotFoundError()
    #     elif response.status >= 400 and response.status <= 499:
    #         raise BaseRequestsException(status_code=response.status)
    #     return {
    #         "status": response.status,
    #         "headers": response.headers,
    #         "body": await response.text(),
    #         "cookies": session.cookie_jar.filter_cookies(self.url)
    #     }