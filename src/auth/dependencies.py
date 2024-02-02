from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = Depends(OAuth2PasswordBearer(tokenUrl="/auth/token"))