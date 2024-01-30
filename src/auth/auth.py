from . import TokenCreater
from requests import auth
from .config import SECRET_KEY, ALGORITHM 
from fastapi.security import OAuth2PasswordRequestForm
        
class Authenticator:

    def __init__(self) -> None:
        self.bazis = auth.BazisMadiRequests()
        self.tokenCreater = TokenCreater(SECRET_KEY, ALGORITHM)

    def authUser(self):
        pass
    

class AppOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):

    def __init__(self, *, 
                 scope:str = "", 
                 login: str, 
                 password: str):
        super().__init__(
            grant_type=None, 
            username=login, 
            password=password, 
            scope=scope, 
            client_id=None, 
            client_secret=None
        )