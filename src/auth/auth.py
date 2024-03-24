from . import TokenCreater, PasswordsManager
from .config import SECRET_KEY, ALGORITHM 
from users.models import UserDBWithPsw, UserRegist, UserInfoDB, UserDBWithHashedPassword, UsersDB
from .exceptions import (
    NotFoundUserError, IncorrectPasswordError,
    UserAlreadyRegistredError, RegistHigherRankingUserError
)
from requests import auth
from users import UserInfoTableInterface, UserTableInterface
from database import SyncDatabaseInterface
from database.schemas import cms as schemas


class Authenticator:

    def __init__(self) -> None:
        self.bazis = auth.BazisMadiRequests()
        self.user_table = UserTableInterface()
        self.user_info_table = UserInfoTableInterface()
        self.user_types_table = SyncDatabaseInterface(schemas.user_type, schemas.sync_engine)
        self.token_creater = TokenCreater(SECRET_KEY, ALGORITHM)
        self.password_manager = PasswordsManager()

    async def is_madi_user(self, user:UserDBWithPsw):
        user = await self.bazis.login(user=user.login, password=user.pwd)
        if not user:
            raise NotFoundUserError(message='This user not found in bazis MADI. Maybe password is wrong.')
        return user
    
    async def auth_user(self, user:UserDBWithPsw):
        db_user = (await self.user_table.get_by_column('login', user.login)).fetchall()
        if not db_user:
            raise NotFoundUserError(message='This user was not found in the database. Please contact your administrator so he can add your account to the system.')
        if not self.password_manager.verify_password(user.pwd, db_user[0].hashed_password):
            raise IncorrectPasswordError(message='Incorrect password.')
        return await self.user_info_table.get_by_column('user_id', db_user[0].id)
    
    async def regist_user(self, user:UserRegist, use_bazis:bool, current_user_type):
        if use_bazis: user.name = await self.is_madi_user(user)
        if (await self.user_info_table.get_by_column('priority', user.priority)).fetchall():
            raise UserAlreadyRegistredError(message='Root user already registred!')
        if (await self.user_table.get_by_column('login', user.login)).fetchall():
            raise UserAlreadyRegistredError()
        if current_user_type.priority < user.priority:
            raise RegistHigherRankingUserError()
        hashed_password = self.password_manager.get_password_hash(user.pwd)
        result = (await self.user_table.add(UserDBWithHashedPassword(
            login=user.login,
            hashed_password=hashed_password
        ))).fetchone()
        print((await self.user_info_table.add(
            UserInfoDB(
                user_id=result.id,
                name=user.name,
                priority = user.priority
            )
        )).fetchone())
        return UsersDB(login=user.login)