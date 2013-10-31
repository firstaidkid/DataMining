import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn import cross_validation
from sklearn import metrics

# Read data from CSV File
energyDataFrame = pd.read_csv('../resources/EnergyMixGeo.csv')
numKeys = len(energyDataFrame);

# extract trainings data and target data 
trainingData = np.array(energyDataFrame[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']])
targetData = energyDataFrame['CO2Emm']

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
svr = SVR(C= 1.0, epsilon= 0.2, kernel='linear')

# Cross Validation Score: -0.032 (+/- 0.013)
# SVR(C=10.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma=0.0,
#   kernel=linear, max_iter=-1, probability=False, random_state=None,
#   shrinking=True, tol=0.001, verbose=False)
# Average Absolute Deviation: 0.00136170016638

# NOT USED ANYMORE : cross_val_score supports Cross-Validation-Parameter, which does the same
# # create kfold
# n_folds = 10
# kf = cross_validation.KFold(numKeys, n_folds=n_folds)

#  # fill cross-validation
# for train_index, test_index in kf:
#  	#print("TRAIN:", train_index, "TEST:", test_index)
#  	X_train, X_test = trainingData[train_index], trainingData[test_index]
#  	y_train, y_test = targetData[train_index], targetData[test_index]

# score
score = cross_validation.cross_val_score(svr, trainingData, targetData, scoring ="mean_squared_error", cv=10)
print "Cross Validation Score: %0.3f (+/- %0.3f)" % (score.mean(), score.std()/2)

# start fitting
fittedData = svr.fit(trainingData, targetData)
#print fittedData

# predict the data
predictedData = svr.predict(trainingData)


# calculate the absolute deviation
absDeviation = predictedData - targetData

MSE=1.0/numKeys*np.sum((predictedData-targetData)**2)
MAD=1.0/numKeys*np.sum(np.abs(predictedData-targetData))
print "Mean Squared Error %2.3f" % (MSE)
print "Mean Absolute Difference %2.3f" % (MAD)

print "Average Absolute Deviation: " + str(absDeviation.mean())

print "\nSVR-Coeficient:"
print svr.coef_

# plt.stem(np.arange(numKeys), absDeviation)
# plt.title('Prediction Error')
# plt.show()

plt.plot(np.arange(numKeys), predictedData, '-r', targetData, '-k')
#plt.show()