import csv
import sqlite3


def initialise_db():

    conn = sqlite3.connect("movie.db")

    c = conn.cursor()

    with open("../ml-latest/movies.csv", "r") as movData:
        dr = csv.DictReader(movData)
        to_ins = [(i["movieId"], i["title"], i["genres"]) for i in dr]

    c.executemany(
        "INSERT INTO movies (movieId, title, genres) VALUES (?, ?, ?)", to_ins
    )

    c.execute("""CREATE TABLE links (
            movieId INTEGER PRIMARY KEY,
            imdbId INTEGER,
            tmdbId INTEGER
        )""")

    with open("../ml-latest/links.csv", "r") as linkData:
        dr = csv.DictReader(linkData)
        to_ins = [(i["movieId"], i["imdbId"], i["tmdbId"]) for i in dr]

    c.executemany(
        "INSERT INTO links (movieId, imdbId, tmdbId) VALUES (?, ?, ?)", to_ins
    )

    conn.commit()

    conn.close()
