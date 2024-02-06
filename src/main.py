from config import ROOT_CMS_NAME, ROOT_CMS_PSWD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from users import router as users_router
from departments import router as department_router
from groups import router as groups_router
from teachers import router as teacher_router


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
app.include_router(department_router.router)
app.include_router(groups_router.router)
app.include_router(teacher_router.router)


@app.on_event('startup')
async def startup_event():
    import auth as auth_module
    from auth import auth
    auth_manager = auth.Authenticator()
    await auth_manager.regist_user(
        auth_module.models.UserDBWithPsw(
            login=ROOT_CMS_NAME,
            pwd=ROOT_CMS_PSWD
        ),
        use_bazis=False
    )