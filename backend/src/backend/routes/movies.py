import logging

from backend.db import ConnectionDep
from backend.exceptions import ReviewAlreadyExistsError, ReviewNotFoundError
from backend.repository import (
    create_review,
    delete_movie_review,
    get_movie_by_id,
    get_movie_by_title,
    get_movies,
    update_review_rating,
)
from backend.routes.auth import GetActiveUserDep
from backend.schemas import Movie, MovieAndReview, Review
from backend.tmdb_api import retrieve_pic
from fastapi import APIRouter, HTTPException, Response, status

# from backend.src.backend.model import createDataset, createModel, getRec

router = APIRouter()
logger = logging.getLogger(__name__)


def get_movie_pics(movies: list[Movie] | list[MovieAndReview]):
    for movie in movies:
        if movie.tmdb_id is not None:
            movie.pic_url = retrieve_pic(movie.tmdb_id)


@router.get("/movies")
def index(user: GetActiveUserDep, con: ConnectionDep) -> list[MovieAndReview]:
    movies = get_movies(con, user.user_id)
    if not movies:
        logger.error("No movies found in database")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occured.",
        )

    get_movie_pics(movies)

    return movies


@router.get("/movies/{movie_title}")
def search(
    movie_title: str, user: GetActiveUserDep, con: ConnectionDep
) -> list[MovieAndReview]:
    movies = get_movie_by_title(con, movie_title, user.user_id)

    if movies:
        get_movie_pics(movies)
    else:
        movies = []

    return movies


"""
@router.get("/movies/{mov_title}")
def search(movie_title: str, user: GetActiveUserDep, con: ConnectionDep) -> list[Movie]:
    movies = get_movie_by_title(con, movie_title, user.user_id)

    if movies:
        get_movie_pics(movies)
    else:
        movies = []

    return movies
"""


@router.post("/rate/{movie_id}/{rating}")
def review(
    movie_id: int, rating: int, user: GetActiveUserDep, con: ConnectionDep
) -> Review:
    movie = get_movie_by_id(con, movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie doesn't exist"
        )
    try:
        rating_obj = create_review(con, user.user_id, movie_id, rating)
    except ReviewAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Movie already has a rating!"
        )
    if not rating_obj:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occured",
        )
    return rating_obj


@router.put("/rate/{movie_id}/{rating}")
def update_rate(
    movie_id: int, rating: int, user: GetActiveUserDep, con: ConnectionDep
) -> Review:
    try:
        rating_obj = update_review_rating(con, user.user_id, movie_id, rating)
    except ReviewNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review doesn't exist"
        )

    return rating_obj


@router.delete("/rate/{movie_id}", status_code=204)
def delete_review(movie_id: int, user: GetActiveUserDep, con: ConnectionDep):
    try:
        delete_movie_review(con, user.user_id, movie_id)
    except ReviewNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review doesn't exist"
        )

    return Response(status_code=204)
