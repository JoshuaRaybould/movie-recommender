from sqlite3 import Connection, IntegrityError

import pandas as pd

from backend.exceptions import UserAlreadyExistsErorr
from backend.schemas import (
    Movie,
    Rating,
    User,
    UserInDB,
)

MOVIES_PER_PAGE = 8


def get_user_id(con: Connection, token: str) -> int | None:
    cur = con.cursor()
    cur.execute("SELECT user_id FROM users WHERE users.user_token = ?", (token,))
    user_id = cur.fetchone()
    if user_id is None:
        return None
    return user_id["user_id"]


def get_movie_by_title(con: Connection, title: str, user_id: int) -> list[Movie]:
    cur = con.cursor()

    cur.execute(
        """
        SELECT movies.movie_id, title, genres, tmdb_id, rating FROM movies 
        INNER JOIN links on movies.movie_id = links.movie_id 
        LEFT OUTER JOIN ratings on movies.movie_id = ratings.movie_id 
        AND ratings.user_id = ? 
        WHERE title LIKE ?
        LIMIT ?
        """,
        (
            user_id,
            "%" + title + "%",
            MOVIES_PER_PAGE,
        ),
    )
    movies = cur.fetchall()
    movie_dicts = map(dict, movies)
    return list(map(Movie.model_validate, movie_dicts))


def get_movies(con: Connection, user_id: int) -> list[Movie]:
    cur = con.execute(
        """
        SELECT movies.movie_id, title, genres, tmdb_id, rating FROM movies 
        INNER JOIN links on movies.movie_id = links.movie_id 
        LEFT OUTER JOIN ratings on movies.movie_id = ratings.movie_id 
        AND ratings.user_id = ? 
        LIMIT ?
        """,
        (
            user_id,
            MOVIES_PER_PAGE,
        ),
    )
    movies = cur.fetchall()
    movie_dicts = map(dict, movies)

    return list(map(Movie.model_validate, movie_dicts))


def get_user_by_username(con: Connection, username: str) -> UserInDB | None:
    cur = con.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    if user is None:
        return None
    return UserInDB.model_validate(dict(user))


def get_user(con: Connection, user_token: str) -> User:
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_token = ?", (user_token,))
    user = cur.fetchone()
    return User.model_validate(dict(user))


def create_user(con: Connection, username: str, hashed_password: str) -> User:
    try:
        cur = con.execute(
            "INSERT INTO users (username, hashed_password) VALUES(?, ?) RETURNING user_id, username, email",
            (username, hashed_password),
        )
        user = cur.fetchone()
        con.commit()
        return User.model_validate(dict(user))
    except IntegrityError:
        raise UserAlreadyExistsErorr


def get_movie_by_id(con: Connection, movie_id: int) -> Movie | None:
    cur = con.execute(
        """
        SELECT movies.movie_id, title, genres, tmdb_id, rating FROM movies 
        INNER JOIN links on movies.movie_id = links.movie_id 
        WHERE movies.movie_id = ? 
        LIMIT 1"
        """,
        (movie_id,),
    )
    movie = cur.fetchone()
    if movie is None:
        return None
    return Movie.model_validate(movie)


def delete_rating(con: Connection, user_id: int, movie_id: int):
    cur = con.cursor()
    cur.execute(
        "DELETE FROM ratings WHERE user_id = ? AND movie_id = ?",
        (user_id, movie_id),
    )


def create_rating(
    con: Connection, user_id: int, movie_id: int, rating: int
) -> Rating | None:
    cur = con.execute(
        "INSERT INTO ratings (user_id, movie_id,  rating) VALUES(?, ?, ?) RETURNING rating_id, movie_id, rating",
        (user_id, movie_id, rating),
    )
    rating_obj = cur.fetchone()
    con.commit()
    if rating_obj is None:
        return None
    return Rating.model_validate(rating_obj)


def get_unreviewed_movies(con: Connection, user_id: int) -> list[Movie]:
    cur = con.execute(
        """
        SELECT movies.movie_id, title, genres, tmdb_id, rating FROM movies
        LEFT OUTER JOIN ratings on movies.movie_id = ratings.movie_id 
        AND ratings.user_id = ? 
        WHERE ratings.rating IS NULL
        """,
        (user_id,),
    )
    unreviwed = cur.fetchall()
    movie_dicts = map(dict, unreviwed)

    return list(map(Movie.model_validate, movie_dicts))


def get_ids_to_reviews_df(con: Connection) -> pd.DataFrame:
    df2 = pd.read_sql_query(
        "SELECT users.user_id, movie_id, rating from ratings INNER JOIN users ON ratings.user_id = users.user_id",
        con,
    )
    return df2


from backend.db import get_connection

if __name__ == "__main__":
    con = get_connection()
    # print(get_movie_by_title(con, "iron", ""))
"""
   movies = get_movies(con, "")
    print(type(movies))
    print(type(movies[0]))
    print(movies) """
# print(create_user(con, "atee"))
