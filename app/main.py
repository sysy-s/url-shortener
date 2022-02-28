from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

from . import models
from .database import engine
from .config import settings
from .routers import url, user, auth, stats

description = """
# URL shortening API

Provides URL creation and customization options as well as:
* User creation and authentication
* Statistics for custom links (only available for users)
"""

app = FastAPI(
    description=description
)


origins = ['http://localhost',
           'http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stats.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(url.router)
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")
