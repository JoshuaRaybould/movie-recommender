import logging
import sqlite3

from dotenv import load_dotenv
from fastapi import HTTPException

from backend.db import ConnectionDep
from backend.main import app
from backend.repository import get_movie_by_title, get_movies
from backend.schemas import Movie
from backend.tmdb_api import retrieve_pic

# from backend.src.backend.model import createDataset, createModel, getRec


load_dotenv()  # todo
logger = logging.getLogger(__name__)


@app.get("/movies/{user_token}")
def index(user_token: str, con: ConnectionDep):
    movies = get_movies(con, user_token)
    if movies is None:
        logger.error("No movies found in database")
        raise HTTPException(status_code=500, detail="An unexpected error occured.")
    movies = [
        {
            "movieId": movieId,
            "title": title,
            "genres": genres,
            "tmdbId": tmdbId,
            "picUrl": retrieve_pic(tmdbId),
            "rating": rating,
        }
        for [movieId, title, genres, imdbId, tmdbId, rating] in movies
    ]
    return movies


@app.get("/movies/{mov_title}/{user_token}")
def search(movie_title: str, user_token, con: ConnectionDep) -> list[Movie]:
    movies = get_movie_by_title(con, movie_title, user_token)
    if movies is None:
        print("BOO")
    if movies:
        movies = [
            {
                "movieId": movieId,
                "title": title,
                "genres": genres,
                "tmdbId": tmdbId,
                "picUrl": retrieve_pic(tmdbId),
                "rating": rating,
            }
            for [movieId, title, genres, imdbId, tmdbId, rating] in movies
        ]
    return movies


@app.post("/signup/{userToken}")
def signup(userToken: str, con: ConnectionDep):
    connection = sqlite3.connect("movie.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE userToken = ?", (userToken,))
    user = cursor.fetchall()
    if user:
        raise HTTPException(status_code=409, detail="duplicate token")
    cursor.execute("INSERT INTO users(userToken) VALUES(?)", (userToken,))
    connection.commit()
    connection.close()
    return userToken


@app.get("/signin/{userToken}")
def signin(userToken: str, con: ConnectionDep):
    connection = sqlite3.connect("movie.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE userToken = ?", (userToken,))
    user = cursor.fetchall()
    if not user:
        raise HTTPException(status_code=404, detail="token doesn't exist")
    connection.close()
    return user


@app.post("/rate/{userToken}/{movieId}/{rating}")
def rate(userToken: str, movieId: int, rating: float, con: ConnectionDep):
    connection = sqlite3.connect("movie.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movies WHERE movieId = ?", (movieId,))
    movie = cursor.fetchall()
    if not movie:
        raise HTTPException(status_code=404, detail="movie doesn't exist")
    cursor.execute("SELECT * FROM users WHERE userToken = ?", (userToken,))
    user = cursor.fetchall()
    if not user:
        raise HTTPException(status_code=404, detail="user doesn't exist")
    cursor.execute(
        "DELETE FROM ratings WHERE userToken = ? AND movieId = ?", (userToken, movieId)
    )
    cursor.execute(
        "INSERT INTO ratings(userToken, movieId,  rating) VALUES(?, ?, ?)",
        (userToken, movieId, rating),
    )
    cursor.execute("SELECT * FROM ratings")
    ratings = cursor.fetchall()
    connection.commit()
    connection.close()
    return ratings


currentModel = None
