from . import TokenCreater, PasswordsManager
from .config import SECRET_KEY, ALGORITHM 
from .models import UserDBWithPsw, UserDBWithHashedPassword, UsersDB
from .exceptions import NotFoundUserError, IncorrectPasswordError
from requests import auth
from database import DatabaseInterface, schemas


class Authenticator:

    def __init__(self) -> None:
        self.bazis = auth.BazisMadiRequests()
        self.db = DatabaseInterface(schemas.user, schemas.cms_engine)
        self.token_creater = TokenCreater(SECRET_KEY, ALGORITHM)
        self.password_manager = PasswordsManager()

    async def is_madi_auth(self, user:UserDBWithPsw):
        if not (await self.bazis.login(user=user.login, password=user.pwd)):
            raise NotFoundUserError(message='This user not found in bazis MADI. Maybe password is wrong.')
        return True
    
    async def auth_user(self, user:UserDBWithPsw):
        db_user = (await self.db.get_by_column('login', user.login))
        if not db_user:
            raise NotFoundUserError(message='This user was not found in the database. Please contact your administrator so he can add your account to the system.')
        if not self.password_manager.verify_password(user.pwd, db_user[0].hashed_password):
            raise IncorrectPasswordError(message='Incorrect password.')
        return True
    
    async def regist_user(self, user:UserDBWithPsw, use_bazis:bool):
        if use_bazis: await self.is_madi_auth(user)
        if not await self.db.get_by_column('login', user.login):
            hashed_password = self.password_manager.get_password_hash(user.pwd)
            await self.db.add(UserDBWithHashedPassword(
                login=user.login,
                hashed_password=hashed_password
            ))
        return UsersDB(login=user.login)