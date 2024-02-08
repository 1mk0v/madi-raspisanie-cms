from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from auth import dependencies
from exceptions import BaseAPIException 
from . import DepartmentTableInterface
from utils import get_pydantic_model

router = APIRouter(
    prefix='/department',
    tags=['Department'],
    dependencies=[dependencies.oauth2_scheme]
)

DepartmentModel:BaseModel = get_pydantic_model(DepartmentTableInterface())

@router.get('/')
async def get_groups(limit:int = 10, offset:int = 0):
    try:
        department_table = DepartmentTableInterface()
        return await department_table.get(limit=limit, offset=offset)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )

@router.post('/add')
async def add_group(data:DepartmentModel): # type: ignore
    try:
        department_table = DepartmentTableInterface()
        res = await department_table.add(data)
        print(res)
        return res
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )
    
@router.delete('/delete/{id}')
async def delete_group(id:int):
    try:
        department_table = DepartmentTableInterface()
        return await department_table.delete(value=id)
    except BaseAPIException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message
        )