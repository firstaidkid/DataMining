import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn import cross_validation

# Read data from CSV File
energyDataFrame = pd.read_csv('../resources/EnergyMixGeo.csv')

# extract trainings data and target data 
trainingData = np.array(energyDataFrame[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']])
targetData = energyDataFrame['CO2Emm']

# create SVR
svr = SVR(kernel='linear')

# create kfold
n_folds = 10
kf = cross_validation.KFold(len(energyDataFrame), n_folds=n_folds)

# fill cross-validation
for train_index, test_index in kf:
	#print("TRAIN:", train_index, "TEST:", test_index)
	X_train, X_test = trainingData[train_index], trainingData[test_index]
	y_train, y_test = targetData[train_index], targetData[test_index]

# score
score = cross_validation.cross_val_score(svr, trainingData, y=targetData, scoring ="mean_squared_error", cv=kf)
print score

# start fitting
fittedData = svr.fit(trainingData, targetData)
print fittedData

# predict the data
predictedData = svr.predict(trainingData)


# calculate the absolute deviation
absDeviation = (targetData.mean() - predictedData.mean());
if absDeviation < 0:
	absDeviation *= -1

print "Absolute Deviation: " + str(absDeviation)