from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import Dict, List
import os
from dotenv import load_dotenv
import requests

load_dotenv()
app = FastAPI()

class Movie(BaseModel):
    title: str
    genres: str
    imdbId: int
    tmdbId: int

@app.get("/{userToken}")
def index(userToken: str):
    connection = sqlite3.connect("movie.db")
    cursor = connection.cursor()
    cursor.execute("SELECT title, genres, imdbId, tmdbId, rating FROM movies INNER JOIN links on movies.movieID = links.movieID LEFT OUTER JOIN ratings on movies.movieId = ratings.movieId AND ratings.userToken = ? LIMIT 8", (userToken,))
    movies = cursor.fetchall()
    connection.close()
    movies = [{"title": title, "genres": genres, "tmdbId": tmdbId, "picUrl": retrievePic(tmdbId), "rating": rating} for [title, genres, imdbId, tmdbId, rating] in movies]
    return movies

@app.get("/movies/{movTitle}/{userToken}")
def search(movTitle: str, userToken):
    print(userToken)
    connection = sqlite3.connect("movie.db")
    cursor = connection.cursor()
    cursor.execute("SELECT title, genres, imdbId, tmdbId, rating FROM movies INNER JOIN links on movies.movieID = links.movieID LEFT OUTER JOIN ratings on movies.movieId = ratings.movieId AND ratings.userToken = ? WHERE title LIKE ? LIMIT 8", (userToken, '%' + movTitle + '%'))
    movies = cursor.fetchall()
    print(movies)
    connection.close()
    movies = [{"title": title, "genres": genres, "tmdbId": tmdbId, "picUrl": retrievePic(tmdbId), "rating": rating} for [title, genres, imdbId, tmdbId, rating] in movies]
    return movies

@app.post("/signup/{userToken}")
def rate(userToken: str):
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
def signin(userToken: str):
    connection = sqlite3.connect("movie.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE userToken = ?", (userToken,))
    user = cursor.fetchall()
    if not user:
        raise HTTPException(status_code=404, detail="token doesn't exist")
    connection.close()
    return user

@app.post("/rate/{userToken}/{movieId}/{rating}")
def rate(userToken: str, movieId: int, rating: float):
    connection = sqlite3.connect("movie.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movies WHERE movieId = ?", (movieId,))
    movie = cursor.fetchall()
    if not movie:
        raise HTTPException(status_code=404, detail="movie doesn't exist")
    cursor.execute("DELETE FROM ratings WHERE userToken = ? AND movieId = ?", (userToken, movieId))
    cursor.execute("INSERT INTO ratings(userToken, movieId,  rating) VALUES(?, ?, ?)", (userToken, movieId, rating))
    cursor.execute("SELECT * FROM ratings")
    ratings = cursor.fetchall()
    connection.commit()
    connection.close()
    return ratings

# Get picture from TMDB
def retrievePic(tmdbId: int):
    url = 'https://api.themoviedb.org/3/movie/' + str(tmdbId)
    headers = {"Authorization": "Bearer " + os.getenv("TMDB_API_KEY"), "accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            pic = data["poster_path"]
            return pic
        else:
            print('Error:', response.status_code)
            return None
    except:
        return None



