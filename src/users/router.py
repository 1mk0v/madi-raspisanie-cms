from fastapi import APIRouter, HTTPException
from auth import dependencies
from exceptions import BaseAPIException
from . import UserTableInterface

router = APIRouter(
    prefix='/users',
    tags=['Users'],
    dependencies=[dependencies.oauth2_scheme]
)

@router.get('/')
async def get_groups(limit:int=10, offset:int=0):
    try:
        usersTable = UserTableInterface()
        return await usersTable.get(limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.delete('/delete')
async def delete_user(id):
    try:
        usersTable = UserTableInterface()
        return await usersTable.delete(id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )