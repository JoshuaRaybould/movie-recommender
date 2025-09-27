import pandas as pd

import heapq
import sqlite3
from surprise import Dataset, SVD, Reader

# First we need to get collect the data from both our MovieLens dataset and our SQL database which has our users and combine into a dataframe we can use
def createDataset():
    df = pd.read_csv("../ml-latest/ratings.csv")

    connection = sqlite3.connect("movie.db")
    df2 = pd.read_sql_query('SELECT userId, movieId, rating from ratings INNER JOIN users ON ratings.userToken = users.userToken', connection)
    connection.close()
    # Importantly we need to ensure there is no overlap on the userIds in the dataset vs our database
    for x in range(0, len(df2["userId"])):
        df2.loc[:,"userId"] = df["userId"] + 400000
    df = pd.concat([df, df2])

    return df


# From training we know that the best parameters were 25 epochs with either 20 or 25 factors, generally 25, with more data 25 is likely to be the best option.
# So we choose 25 epochs and 25 parameters and use everything available.
def createModel(df):
    reader = Reader(rating_scale=(0.5,5))
    movieData = Dataset.load_from_df(df[["userId", "movieId", "rating"]], reader)
    svd = SVD(n_factors=25, n_epochs=25)
    svd.fit(movieData.build_full_trainset())

    return svd

topOpts = {}
def getRec(svd, userToken):

    connection = sqlite3.connect("movie.db")
    cur = connection.cursor()

    cur.execute("SELECT userId FROM users WHERE userToken = ?", (userToken,))
    userId = cur.fetchall()
    userId = userId[0][0] + 400000

    if userId in topOpts and topOpts[userId] != []:
        connection.close()
        return heapq.heappop(topOpts[userId])

    #cur.execute("SELECT movieId FROM movies")
    cur.execute("SELECT movies.movieId, rating FROM movies LEFT OUTER JOIN ratings on movies.movieId = ratings.movieId AND ratings.userToken = ? WHERE ratings.rating IS NULL", (userToken,))
    movieIds = cur.fetchall()

    arr = []
    for movieId in movieIds:
        movId = movieId[0]
        pred = svd.predict(userId, movId)
        estimate = pred.est
        if not arr:
            heapq.heappush(arr, (estimate, movId))
        else:
            heapq.heappush(arr, (estimate, movId))
            if len(arr) > 50:
                heapq.heappop(arr)

    topOpts[userId] = []
    for (est, movId) in arr:
        heapq.heappush(topOpts[userId], (-est, movId))

    if topOpts[userId] != []:
        return heapq.heappop(topOpts[userId])
    return (1,1)


