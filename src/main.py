from config import ROOT_CMS_NAME, ROOT_CMS_PSWD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from users import router as users_router
from groups import router as groups_router
from teachers import router as teacher_router
from schedule import router as schedule_router
from date import router as date_router
from other_tables import router as other_router 

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
app.include_router(groups_router.router)
app.include_router(teacher_router.router)
app.include_router(date_router.router)
app.include_router(schedule_router.router)
app.include_router(other_router.router)




@app.on_event('startup')
async def startup_event():
    from database import DatabaseInterface, schemas
    from users import config, models as user_models
    from auth import auth
    import exceptions as exc

    auth_manager = auth.Authenticator()
    user_type_table = DatabaseInterface(schemas.user_type, schemas.cms_engine)

    if not await user_type_table.get():
        for user_type in config.USER_TYPES:
            await user_type_table.add(user_type)
    try:
        await auth_manager.regist_user(
            user_models.UserRegist(
                login=ROOT_CMS_NAME,
                pwd=ROOT_CMS_PSWD,
                priority=100
            ),
            use_bazis=False,
            current_user_type=user_models.UserType(
                value='APP', priority=101
            )
        )
    except exc.BaseAPIException as error:
        print(error.message)

