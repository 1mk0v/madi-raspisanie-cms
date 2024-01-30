from fastapi import APIRouter
from requests import auth

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/')
async def auth_user():
    bazis = auth.BazisMadiRequests()
    return await bazis.post(user='45645', password="s40E7")