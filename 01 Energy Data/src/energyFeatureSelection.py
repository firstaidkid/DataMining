import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2
from pymaps import *

# Read data from CSV File
energyDataFrame = pd.read_csv('../resources/EnergyMixGeoCluster.csv')
features = np.array(energyDataFrame[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']])
targets = energyDataFrame['CO2Emm']

# create a feateSelector with chi2-function and 3-features
featureSelector = SelectKBest(chi2, 3)

# fit to features and targets
featureSelector.fit(features, targets)

# print the scores
print featureSelector.scores_