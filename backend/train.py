import pandas as pd

from surprise import Dataset, SVD, Reader, accuracy
from surprise.model_selection import cross_validate, train_test_split
from sklearn.model_selection import train_test_split as sk_train_test_split

# Load our dataset
df = pd.read_csv("../movieData/ratings.csv")

# Split into a training set and test set
trainset, testset = sk_train_test_split(df, test_size=0.10)

# Hyperparameter options
n_factors = [20, 25, 30, 45]
n_epochs = [15, 25]

# Prepare the data for reading and read it
reader = Reader(rating_scale=(0.5,5))
trainData = Dataset.load_from_df(trainset[["userId", "movieId", "rating"]], reader)
testData = Dataset.load_from_df(testset[["userId", "movieId", "rating"]], reader)

folds = 5
bestRMSE = float('infinity')
chosenFactor = -1
chosenEpoch = -1

# Search for the best hyperparameters
for factorChoice in n_factors:
    for epochChoice in n_epochs:
        svd = SVD(n_factors=factorChoice, n_epochs=epochChoice)
        print("Current iteration we are using " + str(factorChoice) + " factors and " + str(epochChoice) + " epochs")
        res = cross_validate(svd, trainData, measures=['RMSE'], cv=folds)
        curMeanRMSE = sum(res['test_rmse'])/folds
        print(curMeanRMSE)

        if curMeanRMSE < bestRMSE:
            bestRMSE = curMeanRMSE
            chosenFactor = factorChoice
            chosenEpoch = epochChoice

# Fit the model with our chosen hyperparameters to the training set
print("We chose to use " + str(chosenFactor) + " factors and " + str(chosenEpoch) + " epochs")
print(chosenFactor)
print(chosenEpoch)
movieData = Dataset.load_from_df(df[["userId", "movieId", "rating"]], reader)

svd = SVD(n_factors=chosenFactor, n_epochs=chosenEpoch)
trainData, testData = train_test_split(movieData, test_size=0.10)
svd.fit(trainData)

# Now measure our performance against the test set

predictions = svd.test(testData)
accuracy.rmse(predictions)

# Now that we have chosen our hyperparameters, if we are happy with performance we can retrain on the entire dataset

svd.fit(movieData.build_full_trainset())



# svd.fit(trainset)
# predictions = svd.test(testset)
# accuracy.rmse(predictions)

# trainset = movieData.build_full_trainset()
# svd.fit(trainSet)


