import logging

from fastapi import APIRouter, HTTPException, status

from backend.db import ConnectionDep
from backend.repository import (
    create_rating,
    delete_rating,
    get_movie_by_id,
    get_movie_by_title,
    get_movies,
)
from backend.routes.auth import GetActiveUserDep
from backend.schemas import Movie, Rating
from backend.tmdb_api import retrieve_pic

# from backend.src.backend.model import createDataset, createModel, getRec

router = APIRouter()
logger = logging.getLogger(__name__)


def get_movie_pics(movies: list[Movie]):
    for movie in movies:
        if movie.tmdb_id is not None:
            movie.pic_url = retrieve_pic(movie.tmdb_id)


@router.get("/movies")
def index(user: GetActiveUserDep, con: ConnectionDep):
    movies = get_movies(con, user.user_id)
    if not movies:
        logger.error("No movies found in database")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occured.",
        )

    get_movie_pics(movies)

    return movies


@router.get("/movies/{mov_title}")
def search(movie_title: str, user: GetActiveUserDep, con: ConnectionDep) -> list[Movie]:
    movies = get_movie_by_title(con, movie_title, user.user_id)

    if movies:
        get_movie_pics(movies)
    else:
        movies = []

    return movies


@router.post("/rate/{movie_id}/{rating}")
def rate(
    movie_id: int, rating: int, user: GetActiveUserDep, con: ConnectionDep
) -> Rating:
    movie = get_movie_by_id(con, movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie doesn't exist"
        )

    delete_rating(con, user.user_id, movie_id)
    rating_obj = create_rating(con, user.user_id, movie_id, rating)
    if not rating_obj:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occured",
        )
    return rating_obj


currentModel = None
