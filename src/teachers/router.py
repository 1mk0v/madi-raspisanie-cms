from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from auth import dependencies
from exceptions import BaseAPIException 
from . import TeacherTableInterface
from utils import get_pydantic_model

router = APIRouter(
    prefix='/teacher',
    tags=['Teachers'],
    dependencies=[dependencies.oauth2_scheme]
)

TeacherModel:BaseModel = get_pydantic_model(TeacherTableInterface())

@router.get('/')
async def get_groups(limit:int = 10, offset:int = 0):
    try:
        teacher_table = TeacherTableInterface()
        return await teacher_table.get(limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/add')
async def add_group(data:TeacherModel): # type: ignore
    try:
        teacher_table = TeacherTableInterface()
        return await teacher_table.add(data)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )
    
@router.delete('/delete/{id}')
async def delete_group(id:int):
    try:
        teacher_table = TeacherTableInterface()
        return await teacher_table.add(id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )