from fastapi import APIRouter, HTTPException
from utils import get_pydantic_model
from auth import dependencies
from exceptions import BaseAPIException
from . import TimeTableInterface
from typing import List

router = APIRouter(
    prefix='/time',
    tags=['Time'],
    dependencies=[dependencies.oauth2_scheme]
)

model = get_pydantic_model(TimeTableInterface(ignore_keys=[]))
model_without_id = get_pydantic_model(TimeTableInterface())

@router.get('/', response_model=List[model])
async def get_date(limit:int = 10, offset:int = 0):
    try:
        time_table = TimeTableInterface()
        return await time_table.get(limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/add', response_model=model)
async def add_date(data:model_without_id): #type: ignore
    try:
        time_table = TimeTableInterface()
        return await time_table.add(data)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.delete('/delete/{id}', response_model=int)
async def delete_schedule(id:int):
    try:
        time_table = TimeTableInterface()
        return await time_table.delete(value=id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )