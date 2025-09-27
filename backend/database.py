import sqlite3, csv

conn = sqlite3.connect('movie.db')

c = conn.cursor()

# Create user table
c.execute("""CREATE TABLE users (
    userId INTEGER PRIMARY KEY,
    userToken text
)""")

# Create rating table
c.execute("""CREATE TABLE ratings (
        userToken text,
        movieId integer,
        rating real
    )""")

# Create and populate movies table and also related links table
c.execute("""CREATE TABLE movies (
        movieId integer PRIMARY KEY,
        title text,
        genres text
    )""")

with open('../ml-latest/movies.csv', 'r') as movData:
    dr = csv.DictReader(movData)
    to_ins = [(i['movieId'], i['title'], i['genres']) for i in dr]

c.executemany("INSERT INTO movies (movieId, title, genres) VALUES (?, ?, ?)", to_ins)


c.execute("""CREATE TABLE links (
        movieId INTEGER PRIMARY KEY,
        imdbId INTEGER,
        tmdbId INTEGER
    )""")

with open('../ml-latest/links.csv', 'r') as linkData:
    dr = csv.DictReader(linkData)
    to_ins = [(i['movieId'], i['imdbId'], i['tmdbId']) for i in dr]

c.executemany("INSERT INTO links (movieId, imdbId, tmdbId) VALUES (?, ?, ?)", to_ins)

c.execute("SELECT * FROM movies")


c.execute("SELECT * FROM links")


conn.commit()

conn.close()
