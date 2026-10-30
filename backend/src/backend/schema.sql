CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    email TEXT UNIQUE,
    username TEXT UNIQUE NOT NULL,
    is_disabled INTEGER NOT NULL DEFAULT 0 CHECK (is_disabled IN (0, 1)),
    created_at TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    genres TEXT
) STRICT;

CREATE TABLE IF NOT EXISTS ratings (
    rating_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating > 0 AND rating <= 5),
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
) STRICT;

CREATE TABLE IF NOT EXISTS links (
    movie_id INTEGER PRIMARY KEY,
    imdb_id INTEGER,
    tmdb_id INTEGER,
    FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
) STRICT;