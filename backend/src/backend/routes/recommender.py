from fastapi import APIRouter

router = APIRouter()


@router.post("/train/{userToken}")
def trainModel():
    df = createDataset()
    global currentModel
    currentModel = createModel(df)
    return True


@router.get("/recommendation/{userToken}")
def getRecommendation(userToken: str, conn: ConnectionDep):
    rec = getRec(currentModel, userToken)
    recId = rec[1]

    connection = sqlite3.connect("movie.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT movies.movieId, title, genres, imdbId, tmdbId, rating FROM movies INNER JOIN links on movies.movieId = links.movieId LEFT OUTER JOIN ratings on movies.movieId = ratings.movieId AND ratings.userToken = ? WHERE movies.movieId = ? LIMIT 1",
        (userToken, recId),
    )
    movies = cursor.fetchall()
    connection.close()
    movies = [
        {
            "movieId": movieId,
            "title": title,
            "genres": genres,
            "tmdbId": tmdbId,
            "picUrl": retrievePic(tmdbId),
            "rating": rating,
            "expected": -rec[0],
        }
        for [movieId, title, genres, imdbId, tmdbId, rating] in movies
    ]
    return movies
