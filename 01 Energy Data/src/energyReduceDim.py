import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import manifold

#Read data from CSV File
energyDataFrame = pd.read_csv('../resources/EnergyMixGeo.csv')

# Number of elements in DataFrame
n_neighbors = len(energyDataFrame) - 2;

# create the 2-dimension Transformation
isomap = manifold.Isomap(n_neighbors, 2)
transformedData = isomap.fit_transform(energyDataFrame[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']])

# Plot the isomap
plt.plot(transformedData[:,0], transformedData[:,1], ".k")

# Plot the Country-Names
for z in range(n_neighbors):
	plt.text(transformedData[z,0], transformedData[z,1], energyDataFrame['Country'][z])
plt.show()