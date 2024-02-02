from . import BaseRequests
from bs4 import BeautifulSoup as bs 
class BazisMadiRequests(BaseRequests):

    def __init__(self, url: str = 'https://bazis.madi.ru/{}/login.php') -> None:
        self.none_auth_title = 'Вход в систему'
        super().__init__(url)

    async def login(self, user:str, password:str, url='stud') -> bool:
        response = await super()._post(url, {'usr':user,'psw':password})
        result = bs(response.body, 'lxml').find('title')
        if result.text == self.none_auth_title:
            return False
        return True
