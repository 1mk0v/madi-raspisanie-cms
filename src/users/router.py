from fastapi import APIRouter, HTTPException, Depends
from auth import dependencies, config, models, exceptions
from exceptions import BaseAPIException
from jose import JWTError, jwt
from typing import Annotated, List
from utils import get_pydantic_model
from database import SyncDatabaseInterface
from database.schemas import cms as schemas
from . import UserTableInterface, UserInfoTableInterface
from .exceptions import DeleteYourselfUserError, DeleteHigherRankingUserError

router = APIRouter(
    prefix='/users',
    tags=['Users'],
    dependencies=[dependencies.oauth2_scheme]
)

UserModel = get_pydantic_model(UserTableInterface())
UserInfoModel = get_pydantic_model(UserInfoTableInterface())
UserTypeModel = get_pydantic_model(SyncDatabaseInterface(schemas.user_type, schemas.sync_engine))

@router.get('/', response_model=List[UserModel])
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
    user = (await usersTable.get_by_column('login', token_data.username)).fetchone()
    if user is None:
        raise exceptions.NotFoundUserError()
    return user

async def get_current_user_type(current_user:Annotated[dict, Depends(get_current_user)]):
    try:
        user_info = UserInfoTableInterface()
        return (await user_info.get_user_type(current_user.id)).fetchone()
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.get('/me', response_model=UserModel)
async def get_me(current_user:Annotated[dict, Depends(get_current_user)]):
    try:
        return current_user
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.get('/me/type', response_model=UserTypeModel)
async def get_me(type:Annotated[dict, Depends(get_current_user_type)]):
    try:
        return type
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
        current_user_type = (await users_info_table.get_user_type(current_user.id)).fetchone()
        delete_user_type = (await users_info_table.get_user_type(id)).fetchone()
        print(current_user_type, delete_user_type)
        if current_user_type['priority'] < delete_user_type['priority']:
            raise DeleteHigherRankingUserError()
        await users_info_table.delete('user_id', id)
        return await users_table.delete(value = id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )