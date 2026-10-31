from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Movie Recommender"
    secret_key: str
    database_path: str
    movie_data_path: str
    access_token_expire: int = 30
    algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()  # type: ignore


SettingDep = Annotated[Settings, Depends(get_settings)]
