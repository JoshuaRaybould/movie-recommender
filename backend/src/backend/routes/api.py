import os
import sqlite3

import requests
from backend.db import ConnectionDep
from backend.repository import get_movie_by_title
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# from backend.src.backend.model import createDataset, createModel, getRec


load_dotenv()
app = FastAPI()


class Movie(BaseModel):
    title: str
    genres: str
    imdbId: int
    tmdbId: int


@app.get("/{user_token}")
def index(user_token: str, con: ConnectionDep):
    movies = get_movies(con)
    connection = sqlite3.connect("movie.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT movies.movieId, title, genres, imdbId, tmdbId, rating FROM movies INNER JOIN links on movies.movieId = links.movieId LEFT OUTER JOIN ratings on movies.movieId = ratings.movieId AND ratings.userToken = ? LIMIT 8",
        (user_token,),
    )
    movies = cursor.fetchall()
    connection.close()
    movies = [
        {
            "movieId": movieId,
            "title": title,
            "genres": genres,
            "tmdbId": tmdbId,
            "picUrl": retrievePic(tmdbId),
            "rating": rating,
        }
        for [movieId, title, genres, imdbId, tmdbId, rating] in movies
    ]
    return movies


@app.get("/movies/{mov_title}/{user_token}")
def search(movie_title: str, user_token, con: ConnectionDep):
    movies = get_movie_by_title(con, movie_title, user_token)

    movies = [
        {
            "movieId": movieId,
            "title": title,
            "genres": genres,
            "tmdbId": tmdbId,
            "picUrl": retrievePic(tmdbId),
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


# Get picture from TMDB
def retrievePic(tmdbId: int):
    url = "https://api.themoviedb.org/3/movie/" + str(tmdbId)
    headers = {
        "Authorization": "Bearer " + os.getenv("TMDB_API_KEY"),
        "accept": "application/json",
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            pic = data["poster_path"]
            return pic
        else:
            print("Error:", response.status_code)
            return None
    except:
        return None


currentModel = None


@app.post("/train/{userToken}")
def trainModel():
    df = createDataset()
    global currentModel
    currentModel = createModel(df)
    return True


@app.get("/recommendation/{userToken}")
def getRecommendation(userToken: str, conn: ConnectionDep):
    rec = getRec(currentModel, userToken)
    recId = rec[1]

    connection = sqlite3.connect("movie.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT movies.movieId, title, genres, imdbId, tmdbId, rating FROM movies INNER JOIN links on movies.movieId = links.movieId LEFT OUTER JOIN ratings on movies.movieId = ratings.movieId AND ratings.userToken = ? WHERE movies.movieId = ? LIMIT 1",
        (userToken, recId),
    )
    movies = cursor.fetchall()
    connection.close()
    movies = [
        {
            "movieId": movieId,
            "title": title,
            "genres": genres,
            "tmdbId": tmdbId,
            "picUrl": retrievePic(tmdbId),
            "rating": rating,
            "expected": -rec[0],
        }
        for [movieId, title, genres, imdbId, tmdbId, rating] in movies
    ]
    return movies
