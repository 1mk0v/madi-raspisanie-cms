from fastapi import APIRouter, HTTPException
from auth import dependencies
from exceptions import BaseAPIException
from typing import List
from utils import get_pydantic_model
from . import EventDetailTableInterface

router = APIRouter(
    prefix='/event_detail',
    tags=['Event Details'],
    dependencies=[dependencies.oauth2_scheme]
)

EventDetailModel = get_pydantic_model(EventDetailTableInterface(ignore_keys=[]))

@router.get('/', response_model=List[EventDetailModel])
async def get_schedules(limit:int = 10, offset:int = 0):
    try:
        event_detail_table = EventDetailTableInterface()
        return await event_detail_table.get(limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/add', response_model=EventDetailModel)
async def add_schedule(data:EventDetailModel): #type: ignore
    try:
        schedule_table = EventDetailTableInterface()
        return await schedule_table.add(data)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.delete('/delete/{id}', response_model=int)
async def delete_schedule(id:int):
    try:
        schedule_table = EventDetailTableInterface()
        return await schedule_table.delete(value=id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )