import csv
import os
import sqlite3
from importlib.resources import files
from sqlite3 import Connection
from typing import Annotated

from fastapi import Depends

DB_PATH = os.environ.get("DATABASE_PATH", "movies.db")
DATA_FOLDER = os.environ.get("MOVIE_DATA_PATH", "../ml-latest-small/")


def get_clean_int(val: str) -> int | None:
    val = val.strip()
    if val == "":
        return None
    else:
        return int(val)


def initialise_db():

    sql_script = files("backend").joinpath("schema.sql").read_text("utf-8")
    conn = sqlite3.connect(DB_PATH)

    c = conn.cursor()

    c.executescript(sql_script)

    with open(DATA_FOLDER + "movies.csv", "r") as movData:
        dr = csv.DictReader(movData)
        to_ins = [(int(i["movieId"]), i["title"], i["genres"]) for i in dr]

    c.executemany(
        "INSERT OR IGNORE INTO movies (movie_id, title, genres) VALUES (?, ?, ?)",
        to_ins,
    )

    with open(DATA_FOLDER + "links.csv", "r") as linkData:
        dr = csv.DictReader(linkData)
        to_ins = [
            (
                int(i["movieId"]),
                get_clean_int(i["imdbId"]),
                get_clean_int(i["tmdbId"]),
            )
            for i in dr
        ]

    c.executemany(
        "INSERT OR IGNORE INTO links (movie_id, imdb_id, tmdb_id) VALUES (?, ?, ?)",
        to_ins,
    )

    conn.commit()

    conn.close()


def get_connection():
    db = sqlite3.connect(
        DB_PATH, check_same_thread=False
    )  # Not sure if this could have consequences
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()


ConnectionDep = Annotated[Connection, Depends(get_connection)]

if __name__ == "__main__":
    print("Start")
    initialise_db()
    """db = get_connection()
    cur = db.cursor()
    res = cur.execute("SELECT * FROM movies")
    c = res.fetchall()
    print(c)"""
