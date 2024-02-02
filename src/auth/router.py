from fastapi import APIRouter, Depends, HTTPException
from .auth import Authenticator, AppOAuth2PasswordRequestForm
from .models import UserDBWithPsw
from exceptions import BaseAPIException
from typing import Annotated

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/')
async def auth_user(
    data: Annotated[AppOAuth2PasswordRequestForm, Depends()]
):
    try:
        auth = Authenticator()
        return await auth.authUser(UserDBWithPsw(login=data.username, pwd=data.password))
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )