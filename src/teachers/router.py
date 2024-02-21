from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from auth import dependencies
from exceptions import BaseAPIException 
from . import TeacherTableInterface
from utils import get_pydantic_model
from typing import List

router = APIRouter(
    prefix='/teacher',
    tags=['Teachers'],
    dependencies=[dependencies.oauth2_scheme]
)

TeacherModel:BaseModel = get_pydantic_model(TeacherTableInterface(ignore_keys=[]))

@router.get('/', response_model=List[TeacherModel])
async def get_teachers(limit:int = 10, offset:int = 0):
    try:
        teacher_table = TeacherTableInterface()
        return await teacher_table.get(limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/add', response_model=TeacherModel)
async def add_teacher(data:TeacherModel): # type: ignore
    try:
        teacher_table = TeacherTableInterface()
        return await teacher_table.add(data)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )
    
@router.delete('/delete/{id}', response_model=int)
async def delete_teacher(id:int):
    try:
        teacher_table = TeacherTableInterface()
        return await teacher_table.delete(value=id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )