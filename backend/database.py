import sqlite3, csv

conn = sqlite3.connect('movie.db')

c = conn.cursor()

# Create user table
c.execute("CREATE TABLE users (userToken text);")

# Create rating table
c.execute("""CREATE TABLE ratings (
        userToken text,
        movieId integer,
        rating real
    )""")

# Create and populate movies table and also related links table
c.execute("""CREATE TABLE movies (
        movieId integer,
        title text,
        genres text
    )""")

with open('../movieData/movies.csv', 'r') as movData:
    dr = csv.DictReader(movData)
    to_ins = [(i['movieId'], i['title'], i['genres']) for i in dr]

c.executemany("INSERT INTO movies (movieId, title, genres) VALUES (?, ?, ?)", to_ins)


c.execute("""CREATE TABLE links (
        movieId integer,
        imdbId integer,
        tmdbId integer
    )""")

with open('../movieData/links.csv', 'r') as linkData:
    dr = csv.DictReader(linkData)
    to_ins = [(i['movieId'], i['imdbId'], i['tmdbId']) for i in dr]

c.executemany("INSERT INTO links (movieId, imdbId, tmdbId) VALUES (?, ?, ?)", to_ins)

c.execute("SELECT * FROM movies")
print(c.fetchmany(50))

c.execute("SELECT * FROM links")
print(c.fetchmany(50))

conn.commit()

conn.close()
