CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    user_token TEXT
) STRICT;

CREATE TABLE movies (
    movie_id integer PRIMARY KEY,
    title TEXT NOT NULL,
    genres TEXT,
    imdb_id INTEGER,
    tmdb_id INTEGER
) STRICT;

CREATE TABLE ratings (
    rating_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    movie_id integer NOT NULL,
    rating INTEGER NOT NULL CHECK (rating > 0 AND rating <= 5),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
) STRICT;

