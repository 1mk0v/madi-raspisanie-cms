from fastapi import APIRouter, HTTPException
from auth import dependencies
from exceptions import BaseAPIException
from typing import List
from utils import get_pydantic_model
from .models import LessonInfo, GetScheduleModel
from . import ScheduleTableInterface

router = APIRouter(
    prefix='/schedule',
    tags=['Schedule'],
    dependencies=[dependencies.oauth2_scheme]
)

ScheduleModel = get_pydantic_model(ScheduleTableInterface(ignore_keys=[]))

@router.get('/', response_model=List[GetScheduleModel])
async def get_schedules(limit:int = 10, offset:int = 0):
    try:
        schedule_table = ScheduleTableInterface()
        return await schedule_table.get(limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/add', response_model=ScheduleModel)
async def add_schedule(data:LessonInfo):
    try:
        schedule_table = ScheduleTableInterface()
        return await schedule_table.add(data)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.delete('/delete/{id}', response_model=int)
async def delete_schedule(id:int):
    try:
        schedule_table = ScheduleTableInterface()
        return await schedule_table.delete(value=id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )