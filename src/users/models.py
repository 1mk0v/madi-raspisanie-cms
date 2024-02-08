from pydantic import BaseModel

class UsersDB(BaseModel):
    login:str

class UserDBWithPsw(UsersDB):
    pwd:str

class UserInfoDB(BaseModel):
    user_id:int
    name:str | None
    type_id:int

class UserRegist(UserDBWithPsw):
    name:str | None = None
    type_id:int

class UserDBWithHashedPassword(UsersDB):
    hashed_password:str