import csv
import os
import sqlite3
from importlib.resources import files

DB_PATH = os.environ.get("DATABASE_PATH", "movies.db")


def initialise_db():

    sql_script = files("backend").joinpath("db.sql")
    conn = sqlite3.connect(DB_PATH)

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
