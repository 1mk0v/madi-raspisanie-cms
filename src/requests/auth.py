from . import BaseRequests, HTTPResponse


class BazisMadiRequests(BaseRequests):

    def __init__(self, url: str = 'https://bazis.madi.ru/{}/login.php') -> None:
        super().__init__(url)

    async def post(self, user:str, password:str, url='stud') -> HTTPResponse:
        return await super()._post(url, {'usr':user,'psw':password})
