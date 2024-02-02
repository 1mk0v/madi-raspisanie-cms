from . import TokenCreater
from .config import SECRET_KEY, ALGORITHM 
from .models import UserDBWithPsw
from .exceptions import AuthException
from requests import auth
from fastapi.security import OAuth2PasswordRequestForm
        
class Authenticator:

    def __init__(self) -> None:
        self.bazis = auth.BazisMadiRequests()
        self.tokenCreater = TokenCreater(SECRET_KEY, ALGORITHM)

    async def authUser(self, user:UserDBWithPsw):
        if (await self.bazis.login(user=user.login, password=user.pwd)):
            return self.tokenCreater.getJWT(username=user.login)
        else:
            raise AuthException()
    

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