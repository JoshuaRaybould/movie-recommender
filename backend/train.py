import pandas as pd

from surprise import Dataset, SVD, Reader
from surprise.model_selection import cross_validate
from sklearn.model_selection import train_test_split

# Load our dataset
df = pd.read_csv("../movieData/ratings.csv")
# print(df.head())
trainset, testset = train_test_split(df, test_size=0.10)

# Hyperparameter options
n_factors = [20, 25, 30, 45]
n_epochs = [15, 25]

# Get the data ready for reading
reader = Reader(rating_scale=(1,5))
movieData = Dataset.load_from_df(trainset[["userId", "movieId", "rating"]], reader)

# Split into a training set and test set

folds = 5
bestRMSE = float('infinity')
chosenFactor = -1
chosenEpoch = -1

for factorChoice in n_factors:
    for epochChoice in n_epochs:
        svd = SVD(n_factors=factorChoice, n_epochs=epochChoice)
        print("Current iteration we are using " + str(factorChoice) + " factors and " + str(epochChoice) + " epochs")
        res = cross_validate(svd, movieData, measures=['RMSE'], cv=folds)
        curMeanRMSE = sum(res['test_rmse'])/folds
        print(curMeanRMSE)

        if curMeanRMSE < bestRMSE:
            bestRMSE = curMeanRMSE
            chosenFactor = factorChoice
            chosenEpoch = epochChoice

print("We end with")
print(chosenFactor)
print(chosenEpoch)

# svd.fit(trainset)
# predictions = svd.test(testset)
# accuracy.rmse(predictions)

# trainset = movieData.build_full_trainset()
# svd.fit(trainSet)


