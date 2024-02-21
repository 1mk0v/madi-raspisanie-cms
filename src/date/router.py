from fastapi import APIRouter, HTTPException
from utils import get_pydantic_model
from auth import dependencies
from exceptions import BaseAPIException
from pydantic import BaseModel
from database import DatabaseInterface, schemas
from schedule_time.router import model as time_model
from typing import List
from . import DateTableInterface

router = APIRouter(
    prefix='/date',
    tags=['Date'],
    dependencies=[dependencies.oauth2_scheme]
)

frequency_model = get_pydantic_model(DatabaseInterface(schemas.frequency, engine=schemas.schedule_engine))

class DateModel(BaseModel):
    id:int
    day:str | None
    frequency:frequency_model #type: ignore
    time:time_model #type: ignore

model = get_pydantic_model(DateTableInterface())

@router.get('/', response_model=List[DateModel])
async def get_date(limit:int = 10, offset:int = 0):
    try:
        date_table = DateTableInterface()
        return await date_table.get(limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/add', response_model=List[model])
async def add_date(data:model): #type: ignore
    try:
        date_table = DateTableInterface()
        return await date_table.add(data)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.delete('/delete/{id}', response_model=int)
async def delete_schedule(id:int):
    try:
        date_table = DateTableInterface()
        return await date_table.delete(value=id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )