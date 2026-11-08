from sqlite3 import Connection, IntegrityError, Row

import pandas as pd

from backend.exceptions import (
    ReviewAlreadyExistsError,
    ReviewNotFoundError,
    UserAlreadyExistsErorr,
)
from backend.schemas import (
    Movie,
    MovieAndReview,
    Review,
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


def to_movie_and_review(row: Row) -> MovieAndReview:
    data = dict(row)

    review = Review.model_validate(data) if data["review_id"] is not None else None

    return MovieAndReview.model_validate({**data, "review": review})


def get_movie_by_title(
    con: Connection, title: str, user_id: int
) -> list[MovieAndReview]:
    cur = con.cursor()

    cur.execute(
        """
        SELECT movies.movie_id, title, genres, tmdb_id, rating, review_id, reviews.user_id FROM movies 
        INNER JOIN links on movies.movie_id = links.movie_id 
        LEFT OUTER JOIN reviews on movies.movie_id = reviews.movie_id 
        AND reviews.user_id = ? 
        WHERE title LIKE ?
        LIMIT ?
        """,
        (
            user_id,
            "%" + title + "%",
            MOVIES_PER_PAGE,
        ),
    )
    res = cur.fetchall()

    return [to_movie_and_review(row) for row in res]


def get_movies(con: Connection, user_id: int) -> list[MovieAndReview]:

    cur = con.execute(
        """
        SELECT movies.movie_id, title, genres, tmdb_id, rating, review_id, reviews.user_id FROM movies 
        INNER JOIN links on movies.movie_id = links.movie_id 
        LEFT OUTER JOIN reviews on movies.movie_id = reviews.movie_id 
        AND reviews.user_id = ? 
        LIMIT ?
        """,
        (
            user_id,
            MOVIES_PER_PAGE,
        ),
    )
    res = cur.fetchall()

    return [to_movie_and_review(row) for row in res]


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
        raise UserAlreadyExistsErorr  # todo, consider other errors


def get_movie_by_id(con: Connection, movie_id: int) -> Movie | None:
    cur = con.execute(
        """
        SELECT movies.movie_id, title, genres, tmdb_id FROM movies 
        LEFT JOIN links on movies.movie_id = links.movie_id 
        WHERE movies.movie_id = ? 
        LIMIT 1
        """,
        (movie_id,),
    )
    movie = cur.fetchone()
    if movie is None:
        return None
    return Movie.model_validate(dict(movie))


def create_review(
    con: Connection, user_id: int, movie_id: int, rating: int
) -> Review | None:
    try:
        cur = con.execute(
            "INSERT INTO reviews (user_id, movie_id, rating) VALUES(?, ?, ?) RETURNING user_id, review_id, movie_id, rating",
            (user_id, movie_id, rating),
        )
        review_obj = cur.fetchone()
        con.commit()

        if review_obj is None:
            return None

        return Review.model_validate(dict(review_obj))
    except IntegrityError:
        raise ReviewAlreadyExistsError


def get_unreviewed_movies(con: Connection, user_id: int) -> list[Movie]:
    cur = con.execute(
        """
        SELECT movies.movie_id, title, genres, tmdb_id FROM movies 
        INNER JOIN links on movies.movie_id = links.movie_id 
        LEFT OUTER JOIN reviews on movies.movie_id = reviews.movie_id 
        AND reviews.user_id = ? 
        WHERE reviews.rating IS NULL
        """,
        (user_id,),
    )
    unreviwed = cur.fetchall()
    movie_dicts = map(dict, unreviwed)
    return list(map(Movie.model_validate, movie_dicts))


def get_ids_to_reviews_df(con: Connection) -> pd.DataFrame:
    df2 = pd.read_sql_query(
        "SELECT users.user_id, movie_id, rating from reviews INNER JOIN users ON reviews.user_id = users.user_id",
        con,
    )
    return df2


def update_review_rating(
    con: Connection, user_id: int, movie_id: int, rating: int
) -> Review:
    cur = con.execute(
        "UPDATE reviews SET rating = ? WHERE user_id = ? AND movie_id = ? RETURNING user_id, review_id, movie_id, rating",
        (rating, user_id, movie_id),
    )

    rev = cur.fetchone()
    con.commit()
    if rev is None:
        raise ReviewNotFoundError

    return Review.model_validate(dict(rev))


def delete_movie_review(con: Connection, user_id: int, review_id: int):
    cur = con.cursor()
    cur.execute(
        "DELETE FROM reviews WHERE user_id = ? AND movie_id = ?",
        (user_id, review_id),
    )
    if cur.rowcount == 0:
        raise ReviewNotFoundError
    con.commit()


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
