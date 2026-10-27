CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    user_token TEXT
) STRICT;

CREATE TABLE IF NOT EXISTS movies (
    movie_id integer PRIMARY KEY,
    title TEXT NOT NULL,
    genres TEXT
) STRICT;

CREATE TABLE IF NOT EXISTS ratings (
    rating_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    movie_id integer NOT NULL,
    rating INTEGER NOT NULL CHECK (rating > 0 AND rating <= 5),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
) STRICT;

CREATE TABLE IF NOT EXISTS links (
    movie_id INTEGER PRIMARY KEY,
    imdb_id INTEGER,
    tmdb_id Integer,
    FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
) STRICT;