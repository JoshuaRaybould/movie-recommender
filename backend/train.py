import pandas as pd

from surprise import Dataset, SVD, Reader
from surprise.model_selection import cross_validate

df = pd.read_csv("../movieData/ratings.csv")
print(df.head())

reader = Reader(rating_scale=(1,5))
movieData = Dataset.load_from_df(df[["userId", "movieId", "rating"]], reader)

svd = SVD()

cross_validate(svd, movieData, measures=['RMSE', 'MAE'], cv=5, verbose=True)



