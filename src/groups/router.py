from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from auth import dependencies
from exceptions import BaseAPIException 
from . import GroupTableInterface
from utils import get_pydantic_model
from typing import List

router = APIRouter(
    prefix='/group',
    tags=['Groups'],
    dependencies=[dependencies.oauth2_scheme]
)

GroupModel:BaseModel = get_pydantic_model(GroupTableInterface(ignore_keys=[]))

@router.get('/', response_model=List[GroupModel])
async def get_groups(limit:int = 10, offset:int = 0):
    try:
        group_table = GroupTableInterface()
        return await group_table.get(limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/add', response_model=GroupModel)
async def add_group(data:GroupModel): # type: ignore
    try:
        group_table = GroupTableInterface()
        return await group_table.add(data)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )
    
@router.delete('/delete/{id}', response_model=int)
async def delete_group(id:int):
    try:
        group_table = GroupTableInterface()
        return await group_table.delete(value=id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )