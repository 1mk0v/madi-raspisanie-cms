from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from auth import dependencies
from exceptions import BaseAPIException 
from . import GroupTableInterface
from utils import get_pydantic_model

router = APIRouter(
    prefix='/group',
    tags=['Groups'],
    dependencies=[dependencies.oauth2_scheme]
)

GroupModel:BaseModel = get_pydantic_model(GroupTableInterface())

@router.get('/')
async def get_groups(limit:int = 10, offset:int = 0):
    try:
        group_table = GroupTableInterface()
        return await group_table.get(limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/add')
async def add_group(data:GroupModel): # type: ignore
    try:
        group_table = GroupTableInterface()
        return await group_table.add(data)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )
    
@router.delete('/delete/{id}')
async def delete_group(id:int):
    try:
        group_table = GroupTableInterface()
        return await group_table.delete(id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )