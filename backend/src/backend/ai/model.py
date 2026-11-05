import heapq
from sqlite3 import Connection

import pandas as pd
from backend.config import get_settings
from backend.repository import get_ids_to_reviews_df, get_unreviewed_movies
from backend.schemas import User
from surprise import SVD, Dataset, Reader

USER_OFFSET = 400000

MOVIE_DATA_PATH = get_settings().movie_data_path


# Todo: we want ratings out of 10 since that is how we'll store it in db and may want to improve this model too!
# First we need to get collect the data from both our MovieLens dataset and our SQL database which has our users and combine into a dataframe we can use
def create_dataset(con: Connection) -> pd.DataFrame:
    df1 = pd.read_csv(MOVIE_DATA_PATH + "ratings.csv")

    df2 = get_ids_to_reviews_df(con)

    # Importantly we need to ensure there is no overlap on the userIds in the dataset vs our database
    df1["rating"] = df1["rating"] * 2
    df2["user_id"] = df2["user_id"] + USER_OFFSET

    combined_df = pd.concat([df1, df2])

    return combined_df


# From training we know that the best parameters were 25 epochs with either 20 or 25 factors, generally 25, with more data 25 is likely to be the best option.
# So we choose 25 epochs and 25 parameters and use everything available.
def create_model(df: pd.DataFrame):
    reader = Reader(rating_scale=(0.5, 5))
    movieData = Dataset.load_from_df(df[["user_id", "movie_id", "rating"]], reader)
    svd = SVD(n_factors=25, n_epochs=25)
    svd.fit(movieData.build_full_trainset())

    return svd


def get_model_full(con):
    df = create_dataset(con)
    model = create_model(df)
    return model


topOpts = {}


def get_rec(svd, con: Connection, user: User):

    userId = user.user_id + USER_OFFSET

    if userId in topOpts and topOpts[userId] != []:
        return heapq.heappop(topOpts[userId])

    movies = get_unreviewed_movies(con, user.user_id)

    arr = []
    for movie in movies:
        movie_id = movie.movie_id
        pred = svd.predict(userId, movie_id)
        estimate = pred.est
        if not arr:
            heapq.heappush(arr, (estimate, movie_id))
        else:
            heapq.heappush(arr, (estimate, movie_id))
            if len(arr) > 50:
                heapq.heappop(arr)

    topOpts[userId] = []
    for est, movie_id in arr:
        heapq.heappush(topOpts[userId], (-est, movie_id))

    if topOpts[userId] != []:
        return heapq.heappop(topOpts[userId])
    return (1, 1)


if __name__ == "__main__":
    print("YES")
