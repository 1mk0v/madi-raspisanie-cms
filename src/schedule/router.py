from fastapi import APIRouter, HTTPException
from auth import dependencies
from exceptions import BaseAPIException
from .models import LessonInfo 
from . import ScheduleTableInterface

router = APIRouter(
    prefix='/schedule',
    tags=['Schedule'],
    dependencies=[dependencies.oauth2_scheme]
)

@router.get('/')
async def get_schedules(limit:int = 10, offset:int = 0):
    try:
        schedule_table = ScheduleTableInterface()
        return await schedule_table.get(limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/add')
async def add_schedule(data:LessonInfo):
    try:
        schedule_table = ScheduleTableInterface()
        return await schedule_table.add(data)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.delete('/delete/{id}')
async def delete_schedule(id:int):
    try:
        schedule_table = ScheduleTableInterface()
        return await schedule_table.delete(value=id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )