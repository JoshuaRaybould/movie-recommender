from sqlite3 import Connection

from backend.schemas import Movie

MOVIES_PER_PAGE = 8


def get_user_id(con: Connection, token: str) -> int | None:
    cur = con.cursor()
    cur.execute("SELECT user_id FROM users WHERE users.user_token = ?", (token,))
    user_id = cur.fetchone()
    return user_id


def get_movie_by_title(
    con: Connection, title: str, user_token: str
) -> list[Movie] | None:
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

    return movies


def get_movies(con: Connection, user_token: str) -> list[Movie] | None:
    cur = con.cursor()
    user_id = get_user_id(con, user_token)
    cur.execute(
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
    return movies


from backend.db import get_connection

if __name__ == "__main__":
    con = get_connection()
    print(get_movie_by_title(con, "iron", ""))
    print(get_movies(con, ""))
