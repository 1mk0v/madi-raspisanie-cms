from fastapi import APIRouter, HTTPException
from schedule.models import Essence
from auth import dependencies
from database import DatabaseInterface, schemas
from exceptions import BaseAPIException 

router = APIRouter(
    prefix='/other',
    tags=['Other'],
    dependencies=[dependencies.oauth2_scheme],
)

@router.get('/{table_name}')
async def get_table_data(table_name:str = 'weekday', limit:int = 10, offset:int = 0):
    """
        You can get data to the following tables:
        - auditorium
        - department
        - discipline
        - frequency
        - type
        - weekday
    """
    try:
        schema = eval(f'schemas.{table_name}')
        db_table = DatabaseInterface(table_schema=schema, engine=schemas.schedule_engine)
        return await db_table.get(limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/{table_name}/add')
async def add_group(value:str, department_id:int = None, table_name:str = 'weekday'): # type: ignore
    """
        You can add data to the following tables:
        - auditorium
        - department
        - discipline
        - frequency
        - type
        - weekday
    """
    try:
        schema = eval(f'schemas.{table_name}')
        db_table = DatabaseInterface(table_schema=schema, engine=schemas.schedule_engine, ignore_keys=["id"])
        return await db_table.add(db_table.model.parse_obj({'value':value, "department_id":department_id}))
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )
    
@router.delete('/{table_name}/delete/{id}')
async def delete_group(id:int, table_name:str = 'weekdays'):
    try:
        schema = eval(f'schemas.{table_name}')
        db_table = DatabaseInterface(table_schema=schema, engine=schemas.schedule_engine, ignore_keys=["id"])
        return await db_table.delete(value=id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )