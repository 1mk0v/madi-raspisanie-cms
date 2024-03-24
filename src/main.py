from config import ROOT_CMS_NAME, ROOT_CMS_PSWD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from users import router as users_router
from community import router as community_router
from event import router as event_router
from event_detail import router as event_detail_router

app = FastAPI(
    title='MADI Raspisanie CMS',
    version="0.1.0",
    contact={
        "name": "Potapchuk Danila Antonovich",
        "url": "https://t.me/nivicki",
        "email": "potapchuk01@mail.ru"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(community_router.router)
app.include_router(event_router.router)
app.include_router(event_detail_router.router)




# @app.on_event('startup')
# async def startup_event():
#     from database import SyncDatabaseInterface
#     from database.schemas import cms
#     from users import config, models as user_models
#     from auth import auth
#     import exceptions as exc

#     auth_manager = auth.Authenticator()
#     user_type_table = SyncDatabaseInterface(cms.user_type, cms.sync_engine)
#     if not await user_type_table.get():
#         for user_type in config.USER_TYPES:
#             await user_type_table.add(user_type)
#     try:
#         await auth_manager.regist_user(
#             user_models.UserRegist(
#                 login=ROOT_CMS_NAME,
#                 pwd=ROOT_CMS_PSWD,
#                 priority=100
#             ),
#             use_bazis=False,
#             current_user_type=user_models.UserType(
#                 value='APP', priority=101
#             )
#         )
#     except exc.BaseAPIException as error:
#         print(error.message)

