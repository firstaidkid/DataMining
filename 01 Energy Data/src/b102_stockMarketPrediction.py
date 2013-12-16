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
predictDuration = 30
predictedData = list()

for i in range(predictDuration):

    predictVector = np.zeros((timeDelay))

    # how many value do we need to take from the targets?
    nrOfTargets = timeDelay - i
    if nrOfTargets < 0:
        nrOfTargets = 0

    # fill predictVector with data from targets
    for j in range(nrOfTargets):
        indexInTargets = 650-timeDelay+j
        predictVector[j] = cyclicYahoo[indexInTargets, -1]

    # now add all already predicted values // Pretty sure an error here: nrOfTargets+1 or something
    for k in range(len(predictedData)):
        predictVector[nrOfTargets+k] = predictedData[k]

        # stop after 24 values in total
        if k >= 23:
            break

    # predict the data using trainings-data from the SVR
    predictedData.append(svr.predict(predictVector)[0])

# print data from 651 > 680
print predictedData

# calculate the absolute deviation
absDeviation = predictedData - targets[len(targets)-predictDuration:]
meanAbsDevitation = absDeviation.mean()
if meanAbsDevitation < 0:
    meanAbsDevitation *= -1
print "\nMean Absolute Deviation: %0.3f" % meanAbsDevitation

