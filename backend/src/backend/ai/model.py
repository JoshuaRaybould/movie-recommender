import heapq
from sqlite3 import Connection

import pandas as pd
from surprise import SVD, Dataset, Reader

from backend.config import get_settings
from backend.db import get_connection
from backend.repository import get_ids_to_reviews_df, get_unreviewed_movies
from backend.schemas import User

USER_OFFSET = 400000

MOVIE_DATA_PATH = get_settings().movie_data_path


# Todo: we want ratings out of 10 since that is how we'll store it in db and may want to improve this model too!
# First we need to get collect the data from both our MovieLens dataset and our SQL database which has our users and combine into a dataframe we can use
def create_dataset(con: Connection) -> pd.DataFrame:
    df1 = pd.read_csv(MOVIE_DATA_PATH + "ratings.csv")
    df1.rename(columns={"movieId": "movie_id", "userId": "user_id"}, inplace=True)

    df2 = get_ids_to_reviews_df(con)

    # Importantly we need to ensure there is no overlap on the userIds in the dataset vs our database
    df1["rating"] = df1["rating"] * 2
    df2["user_id"] = df2["user_id"] + USER_OFFSET

    combined_df = pd.concat([df1, df2])

    return combined_df


# From training we know that the best parameters were 25 epochs with either 20 or 25 factors, generally 25, with more data 25 is likely to be the best option.
# So we choose 25 epochs and 25 parameters and use everything available.
def create_model(df: pd.DataFrame):
    reader = Reader(rating_scale=(1, 10))
    movieData = Dataset.load_from_df(df[["user_id", "movie_id", "rating"]], reader)
    svd = SVD(n_factors=25, n_epochs=25)
    svd.fit(movieData.build_full_trainset())

    return svd


def get_model_full(con):
    df = create_dataset(con)
    model = create_model(df)
    return model


topOpts = {}


def get_rec(svd, con: Connection, user: User) -> dict | None:

    user_id = user.user_id + USER_OFFSET

    if user_id in topOpts and topOpts[user_id] != []:
        rec = heapq.heappop(topOpts[user_id])
        return {"movie_id": rec[1], "expected_score": -rec[0]}

    movies = get_unreviewed_movies(con, user.user_id)

    arr = []
    for movie in movies:
        movie_id = movie.movie_id
        pred = svd.predict(user_id, movie_id)
        estimate = pred.est

        if not arr:
            heapq.heappush(arr, (estimate, movie_id))
        else:
            heapq.heappush(arr, (estimate, movie_id))
            if len(arr) > 10:
                heapq.heappop(arr)

    topOpts[user_id] = []
    for est, movie_id in arr:
        heapq.heappush(topOpts[user_id], (-est, movie_id))

    if topOpts[user_id] != []:
        rec = heapq.heappop(topOpts[user_id])
        return {"movie_id": rec[1], "expected_score": -rec[0]}
    return None


if __name__ == "__main__":
    con = get_connection()
    create_dataset(con)
