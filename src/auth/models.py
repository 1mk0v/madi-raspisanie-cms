from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []

class UsersDB(BaseModel):
    login:str

class UserDBWithPsw(UsersDB):
    pwd:str

class UserDBWithHashedPassword(UsersDB):
    hashed_password:str