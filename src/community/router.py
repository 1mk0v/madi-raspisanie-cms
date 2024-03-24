from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from auth import dependencies
from exceptions import BaseAPIException 
from . import GroupTableInterface, TeacherTableInterface
from .dependencies import current_year
from utils import get_pydantic_model
from typing import List

router = APIRouter(
    prefix='/community',
    tags=['Community'],
    dependencies=[dependencies.oauth2_scheme]
)

CommunityModel:BaseModel = get_pydantic_model(GroupTableInterface(ignore_keys=[]))

@router.get('/group', response_model=List[CommunityModel])
async def get_groups(year:int = Depends(current_year), limit:int = 10, offset:int = 0):
    try:
        group_table = GroupTableInterface()
        return await group_table.get_by_column(columnName='year', value=year, limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/group/add', response_model=CommunityModel)
async def add_group(data:CommunityModel): # type: ignore
    try:
        group_table = GroupTableInterface()
        return await group_table.add(data)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.delete('/group/delete/{id}', response_model=int)
async def delete_group(id:int):
    try:
        group_table = GroupTableInterface()
        return await group_table.delete(value=id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.get('/teacher', response_model=List[CommunityModel])
async def get_teachers(year:int = Depends(current_year), limit:int = 10, offset:int = 0):
    try:
        teacher_table = TeacherTableInterface()
        return await teacher_table.get_by_column(columnName='year', value=year, limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/teacher/add', response_model=CommunityModel)
async def add_teacher(data:CommunityModel): # type: ignore
    try:
        teacher_table = TeacherTableInterface()
        return await teacher_table.add(data)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )
    
@router.delete('/teacher/delete/{id}', response_model=int)
async def delete_teacher(id:int):
    try:
        teacher_table = TeacherTableInterface()
        return await teacher_table.delete(value=id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )
    
@router.get('/{community}', deprecated=True)
async def get_communities(community:str, limit:int = 10, offset:int = 0):
    try:
        pass
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/{community}/add', deprecated=True)
async def add_community(community:str, data:CommunityModel): # type: ignore
    try:
        pass
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )
    
@router.delete('/{community}/delete/{id}', deprecated=True)
async def delete_community(community:str, id:int):
    try:
        pass
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )