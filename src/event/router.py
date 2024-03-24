from fastapi import APIRouter, HTTPException
from auth import dependencies
from exceptions import BaseAPIException
from typing import List
from utils import get_pydantic_model
from .utils import get_validated_data
from .models import LessonInfo
from . import EventTableInterface

router = APIRouter(
    prefix='/event',
    tags=['Events'],
    dependencies=[dependencies.oauth2_scheme]
)

ScheduleModel = get_pydantic_model(EventTableInterface(ignore_keys=[]))

@router.get('/', response_model=List[LessonInfo])
async def get_schedules(limit:int = 10, offset:int = 0):
    try:
        schedule_table = EventTableInterface()
        return get_validated_data(await schedule_table.get_lessons(limit=limit, offset=offset))
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/add', response_model=ScheduleModel)
async def add_schedule(data:LessonInfo):
    try:
        schedule_table = EventTableInterface()
        return await schedule_table.add(data)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.delete('/delete/{id}', response_model=int)
async def delete_schedule(id:int):
    try:
        schedule_table = EventTableInterface()
        return await schedule_table.delete(value=id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )