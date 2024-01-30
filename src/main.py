from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router

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
