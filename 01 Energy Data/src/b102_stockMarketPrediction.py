import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn import cross_validation


def createCyclicData(data, timeDelay):
    # create an array with the shape nrValues X timeDelay+Value
    result = np.zeros((len(data),timeDelay+1))

    # timedelay too small, return current data
    if timeDelay == 0:
        return data

    # go through each data-row
    for i in range(len(data)):
        #print "i:\t\t%d" % i

        # get the i-timeDelay values as input-attributes
        for j in range(timeDelay+1):
            # calculate index of item
            index = i - (timeDelay-j)

            # ring around the rosy
            if index < 0:
                index = len(data) + index

            #print "index:\t%d" % index

            # put value into result-index
            result[i,j] = data[index]

    return result


# read dataframe from file
df = pd.DataFrame.from_csv("../resources/effectiveRates.csv")

# Choose five companies
cleanedDataframe = df[['AMZN', 'MSFT', 'AAPL', 'YHOO', 'SAP']]

# Plot those
cleanedDataframe.plot()
plt.show()

# Choose yahoo
yahooDf = df['YHOO']

timeDelay = 24
cyclicYahoo = createCyclicData(yahooDf, timeDelay)

# extract features and targets from data, use first 650 rows for training
features = np.array(cyclicYahoo[:650,:timeDelay])
targets = cyclicYahoo[:650, timeDelay:].reshape((650))

# Create SVR with given settings
svr = SVR(C= 500.0, epsilon= 0.3, kernel='rbf')

# start fitting
fittedData = svr.fit(features, targets)

# data to predict: last 30 days
predict = cyclicYahoo[len(cyclicYahoo)-30:, :timeDelay]

# predict the data using trainings-data from the SVR
predictedData = svr.predict(predict)

# calculate the absolute deviation
absDeviation = predictedData - targets[len(targets)-30:]
meanAbsDevitation = absDeviation.mean()
if meanAbsDevitation < 0:
    meanAbsDevitation *= -1
print "\nMean Absolute Deviation: %0.3f" % meanAbsDevitation

