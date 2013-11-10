import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn import cross_validation
from sklearn import metrics

np.set_printoptions(precision=3)

# Read data from CSV File
energyDataFrame = pd.read_csv('../resources/EnergyMixGeo.csv')
numKeys = len(energyDataFrame);

# extract trainings data and target data 
features = np.array(energyDataFrame[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']])
targets = energyDataFrame['CO2Emm']

# create SVR
# Standard Configuration
#svr = SVR(C= 1.0, epsilon= 0.1, kernel='linear')
# Cross Validation Score: -0.032 (+/- 0.013)
# SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma=0.0,
#   kernel=linear, max_iter=-1, probability=False, random_state=None,
#   shrinking=True, tol=0.001, verbose=False)
# Average Absolute Deviation: 0.00221559082899

# The original SVM formulations for Regression (SVR) used parameters C [0, inf) and epsilon[0, inf) to apply a penalty to the optimization for points which were not correctly predicted.

# Best Configuration:
svr = SVR(C= 5.0, epsilon= 0.109, kernel='linear')

# score
scores = cross_validation.cross_val_score(svr, features, targets, scoring ="mean_squared_error", cv=10)
print "Cross Validation Score for each Iteration:"
print scores
print "\nCross Validation Score Mean: %0.3f (+/- %0.3f)" % (scores.mean(), scores.std()/2)

# start fitting
fittedData = svr.fit(features, targets)
#print fittedData

# predict the data using trainings-data from the SVR
predictedData = svr.predict(features)

# calculate the absolute deviation
absDeviation = predictedData - targets
meanAbsDevitation = absDeviation.mean();
if meanAbsDevitation < 0:
	meanAbsDevitation *= -1
print "\nMean Absolute Deviation: %0.3f" % (meanAbsDevitation)

print "\nSVR-Coefficients:"
print svr.coef_

#plt.stem(np.arange(numKeys), absDeviation)
#plt.title('Prediction Error')
#plt.show()

plt.plot(np.arange(numKeys), predictedData, '-r', targets, '-k')
plt.show()