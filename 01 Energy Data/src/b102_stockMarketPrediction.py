import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn import cross_validation


def createCyclicData(data, timeDealy):

    return data


# read dataframe from file
df = pd.DataFrame.from_csv("../resources/effectiveRates.csv")

# Choose five companies
cleanedDataframe = df[['AMZN', 'MSFT', 'AAPL', 'YHOO', 'SAP']]

# Plot those
cleanedDataframe.plot()
plt.show()

# Choose yahoo
yahooDf = df['YHOO']

# extract features and targets from data
features = yahooDf[:650]
targets = yahooDf[650:]

# Create SVR with given settings
svr = SVR(C= 500.0, epsilon= 0.3, kernel='rbf')

# start fitting
fittedData = svr.fit(features, targets)

# predict the data using trainings-data from the SVR
predictedData = svr.predict(features)

# calculate the absolute deviation
absDeviation = predictedData - targets
meanAbsDevitation = absDeviation.mean()
if meanAbsDevitation < 0:
    meanAbsDevitation *= -1
print "\nMean Absolute Deviation: %0.3f" % meanAbsDevitation
