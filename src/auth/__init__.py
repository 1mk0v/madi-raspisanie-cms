from datetime import timedelta, datetime
from jose import jwt
from passlib.context import CryptContext
from .models import Token

class TokenCreater:

    def __init__(
            self,
            secret_key:str,
            algorithm:str,
            token_access_minutes:int=30  
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_access_minutes = token_access_minutes

    def getJWT(self, username:str, scopes:list = ['']) -> Token:
        access_token_expires = timedelta(minutes=self.token_access_minutes)
        access_token = self.create_access_token(
            data={"sub": username, "scopes": " ".join(scopes)},
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type='bearer')

    def create_access_token(self, data: dict, expires_delta: timedelta | None = timedelta(minutes=15)):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
class PasswordsManager:
    def __init__(
            self, 
            schemes:list=["bcrypt"], 
            deprecated:str="auto") -> None:
        self.context = CryptContext(schemes=schemes, deprecated=deprecated)

    def verify_password(self, plain_password, hashed_password):
        return self.context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password):
        return self.context.hash(password)