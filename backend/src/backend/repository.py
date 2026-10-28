from sqlite3 import Connection

from backend.exceptions import UserAlreadyExistsErorr
from backend.schemas import Movie, Rating, User

MOVIES_PER_PAGE = 8


def get_user_id(con: Connection, token: str) -> int | None:
    cur = con.cursor()
    cur.execute("SELECT user_id FROM users WHERE users.user_token = ?", (token,))
    user_id = cur.fetchone()
    if user_id is None:
        return None
    return user_id["user_id"]


def get_movie_by_title(con: Connection, title: str, user_token: str) -> list[Movie]:
    user_id = get_user_id(con, user_token)
    cursor = con.cursor()

    cursor.execute(
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
    movies = cursor.fetchall()
    movie_dicts = map(dict, movies)
    return list(map(Movie.model_validate, movie_dicts))


def get_movies(con: Connection, user_token: str) -> list[Movie]:
    user_id = get_user_id(con, user_token)
    cur = con.execute(
        """
        SELECT movies.movie_id, title, genres, tmdb_id FROM movies 
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


def get_user(con: Connection, user_token: str) -> User:
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_token = ?", (user_token,))
    user = cur.fetchone()
    return User.model_validate(dict(user))


def create_user(con: Connection, user_token: str) -> User:
    try:
        cur = con.execute(
            "INSERT INTO users (user_token) VALUES(?) RETURNING user_id, user_token",
            (user_token,),
        )
        user = cur.fetchone()
        con.commit()
        return User.model_validate(dict(user))
    except:
        raise UserAlreadyExistsErorr


def get_movie_by_id(con: Connection, movie_id: int) -> Movie:
    cur = con.execute("SELECT * FROM movies WHERE movie_id = ?", (movie_id,))
    movie = cur.fetchone()
    return Movie.model_validate(movie)


def delete_rating(con: Connection, user_token: str, movie_id: int):
    cur = con.cursor()
    cur.execute(
        "DELETE FROM ratings WHERE user_token = ? AND movie_id = ?",
        (user_token, movie_id),
    )


def create_rating(
    con: Connection, user_token: str, movie_id: int, rating: int
) -> Rating:
    cur = con.execute(
        "INSERT INTO ratings (user_token, movie_id,  rating) VALUES(?, ?, ?) RETURNING rating_id, movie_id, rating",
        (user_token, movie_id, rating),
    )
    rating_obj = cur.fetchone()
    con.commit()
    return Rating.model_validate(rating_obj)


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
