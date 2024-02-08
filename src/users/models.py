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
    priority:int

class UserDBWithHashedPassword(UsersDB):
    hashed_password:str

class UserType(BaseModel):
    value:str
    priority:int