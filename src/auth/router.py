from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .auth import Authenticator
from .models import UserDBWithPsw, Token, UsersDB
from .dependencies import oauth2_scheme
from exceptions import BaseAPIException
from typing import Annotated

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/token')
async def auth_user(
    data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    try:
        auth = Authenticator()
        await auth.auth_user(UserDBWithPsw(login=data.username, pwd=data.password))
        return auth.token_creater.getJWT(data.username, data.scopes)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )
    
@router.post('/registration', dependencies=[oauth2_scheme])
async def register_user(user:UserDBWithPsw, 
                        use_bazis:bool = False) -> UsersDB:
    try:
        auth = Authenticator()
        return await auth.regist_user(user, use_bazis)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )