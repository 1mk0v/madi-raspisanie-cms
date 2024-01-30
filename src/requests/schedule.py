from . import BaseRequests, HTTPResponse
from .exceptions import BaseRequestsException

class MADIRaspisanieAPI(BaseRequests):

    def __init__(self, url: str = 'http://127.0.0.1:8888/{}') -> None:
        super().__init__(url)

    async def get(self, url) -> HTTPResponse:
        return await super()._get(url)