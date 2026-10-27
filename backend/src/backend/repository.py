from sqlite3 import Connection


def get_movie_by_title(con: Connection, title: str, user_token: str):
    cursor = con.cursor()

    cursor.execute(
        "SELECT movies.movieId, title, genres, imdbId, tmdbId, rating FROM movies INNER JOIN links on movies.movieID = links.movieID LEFT OUTER JOIN ratings on movies.movieId = ratings.movieId AND ratings.userToken = ? WHERE title LIKE ? LIMIT 8",
        (
            user_token,
            "%" + title + "%",
        ),
    )
    movies = cursor.fetchall()

    return movies
