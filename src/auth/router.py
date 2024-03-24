from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from users.models import UserDBWithPsw, UserRegist, UsersDB
from users import router as user_router
from .auth import Authenticator
from .models import Token
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
async def register_user(
    user:UserRegist,
    current_user_type: Annotated[dict, Depends(user_router.get_current_user_type)],
    use_bazis:bool = False
) -> UsersDB:
    try:
        auth = Authenticator()
        return await auth.regist_user(user, use_bazis, current_user_type)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )