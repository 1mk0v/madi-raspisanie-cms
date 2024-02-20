from fastapi import APIRouter, HTTPException
from utils import get_pydantic_model
from auth import dependencies
from exceptions import BaseAPIException
from . import DateTableInterface

router = APIRouter(
    prefix='/date',
    tags=['Date'],
    dependencies=[dependencies.oauth2_scheme]
)

model = get_pydantic_model(DateTableInterface())

@router.get('/')
async def get_date(limit:int = 10, offset:int = 0):
    try:
        date_table = DateTableInterface()
        return await date_table.get(limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/add')
async def add_date(data:model): #type: ignore
    try:
        date_table = DateTableInterface()
        return await date_table.add(data)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.delete('/delete/{id}')
async def delete_schedule(id:int):
    try:
        date_table = DateTableInterface()
        return await date_table.delete(value=id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )