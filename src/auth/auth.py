from . import TokenCreater
from .config import SECRET_KEY, ALGORITHM 
from .models import UserDBWithPsw
from .exceptions import AuthException
from requests import auth, exceptions as request_exception
from database import DatabaseInterface, schemas
from fastapi.security import OAuth2PasswordRequestForm
        
class Authenticator:

    def __init__(self) -> None:
        self.bazis = auth.BazisMadiRequests()
        self.db = DatabaseInterface(schemas.user, schemas.cms_engine)
        self.tokenCreater = TokenCreater(SECRET_KEY, ALGORITHM)

    async def authUser(self, user:UserDBWithPsw):
        try:
            if await self.bazis.login(user=user.login, password=user.pwd):
                return True
            else:
                raise AuthException()
        except request_exception.BaseRequestsException as error:
            print(await self.db.get())
            raise AuthException(message=error.message, status_code=error.status_code)

    

class AppOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(self, *, 
                 grant_type: str | None = None, 
                 login: str, 
                 password: str, 
                 scope: str = "", 
                 client_id: str | None = None, 
                 client_secret: str | None = None):
        super().__init__(
            grant_type=grant_type, 
            username=login, 
            password=password, 
            scope=scope, 
            client_id=client_id, 
            client_secret=client_secret
        )