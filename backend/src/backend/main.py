import sqlite3
import typing
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI

from backend.ai_model import get_model_full
from backend.config import get_settings
from backend.db import initialise_db
from backend.routes import auth, movies

DB_PATH = get_settings().database_path


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialise_db()
    with sqlite3.connect(DB_PATH) as db:
        app.state.model = get_model_full(db)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(movies.router)
# app.include_router(recommender.router)


def get_model():
    return app.state.model


ModelDep = Annotated[typing.Any, Depends(get_model)]
