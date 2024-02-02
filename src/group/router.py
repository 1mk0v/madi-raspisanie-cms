from fastapi import APIRouter
from auth import dependencies
from . import GroupTableInterface

router = APIRouter(
    prefix='/group',
    tags=['Groups'],
    dependencies=[dependencies.oauth2_scheme]
)

@router.get('/')
async def get_groups():
    groupTable = GroupTableInterface()
    return groupTable.get()
