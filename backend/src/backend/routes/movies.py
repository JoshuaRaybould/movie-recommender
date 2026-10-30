import logging

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from backend.db import ConnectionDep
from backend.repository import (
    create_rating,
    delete_rating,
    get_movie_by_id,
    get_movie_by_title,
    get_movies,
    get_user,
)
from backend.schemas import Movie, Rating
from backend.tmdb_api import retrieve_pic

# from backend.src.backend.model import createDataset, createModel, getRec

router = APIRouter()
load_dotenv()  # todo
logger = logging.getLogger(__name__)


def get_movie_pics(movies: list[Movie]):
    for movie in movies:
        if movie.tmdb_id is not None:
            movie.pic_url = retrieve_pic(movie.tmdb_id)


@router.get("/movies/{user_token}")
def index(user_token: str, con: ConnectionDep):
    movies = get_movies(con, user_token)
    if not movies:
        logger.error("No movies found in database")
        raise HTTPException(status_code=500, detail="An unexpected error occured.")

    get_movie_pics(movies)

    return movies


@router.get("/movies/{mov_title}/{user_token}")
def search(movie_title: str, user_token, con: ConnectionDep) -> list[Movie]:
    movies = get_movie_by_title(con, movie_title, user_token)

    if movies:
        get_movie_pics(movies)
    else:
        movies = []

    return movies


@router.post("/rate/{user_token}/{movie_id}/{rating}")
def rate(user_token: str, movie_id: int, rating: int, con: ConnectionDep) -> Rating:
    movie = get_movie_by_id(con, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie doesn't exist")

    user = get_user(con, user_token)
    if not user:
        raise HTTPException(status_code=404, detail="User (token) doesn't exist")

    delete_rating(con, user_token, movie_id)
    rating_obj = create_rating(con, user_token, movie_id, rating)
    if not rating_obj:
        raise HTTPException(status_code=500, detail="An unexpected error occured")
    return rating_obj


currentModel = None
