from config import ROOT_CMS_NAME, ROOT_CMS_PSWD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from group import router as group_router

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
app.include_router(group_router.router)


@app.on_event('startup')
async def startup_event():
    import auth as auth_module
    from auth import auth
    auth_manager = auth.Authenticator()
    await auth_manager.regist_user(
        auth_module.models.UserDBWithPsw(
            login=ROOT_CMS_NAME,
            pwd=ROOT_CMS_PSWD
        )
    )