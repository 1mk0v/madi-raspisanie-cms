from fastapi import APIRouter, HTTPException, Depends
from auth import dependencies, config, models, exceptions
from exceptions import BaseAPIException
from jose import JWTError, jwt
from typing import Annotated
from . import UserTableInterface, UserInfoTableInterface
from .exceptions import DeleteYourselfUserError, DeleteHigherRankingUserError

router = APIRouter(
    prefix='/users',
    tags=['Users'],
    dependencies=[dependencies.oauth2_scheme]
)

@router.get('/')
async def get_users(limit:int=10, offset:int=0):
    try:
        usersTable = UserTableInterface()
        return await usersTable.get(limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )


async def get_current_user(token: Annotated[str, dependencies.oauth2_scheme]):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise exceptions.AuthException()
        token_data = models.TokenData(username=username)
    except JWTError as error:
        raise BaseAPIException(message=error.args, status_code=500)
    usersTable = UserTableInterface()
    user = await usersTable.get_by_column('login', token_data.username)
    if user is None:
        raise exceptions.NotFoundUserError()
    return user[0]


@router.get('/me')
async def get_me(current_user:Annotated[dict, Depends(get_current_user)]):
    try:
        return current_user
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.delete('/delete')
async def delete_user(id:int, current_user:Annotated[dict, Depends(get_current_user)]):
    try:
        if current_user.id == id:
            raise DeleteYourselfUserError()
        users_table = UserTableInterface()
        users_info_table = UserInfoTableInterface()
        current_user_type = await users_info_table.get_user_type(current_user.id)
        delete_user_type = await users_info_table.get_user_type(id)
        if current_user_type['priority'] < delete_user_type['priority']:
            raise DeleteHigherRankingUserError()
        await users_info_table.delete('user_id', id)
        return await users_table.delete(value = id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )