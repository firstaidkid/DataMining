import numpy as np
import pandas as pd
from sklearn import preprocessing
from scipy.cluster.hierarchy import *
from scipy.spatial.distance import *
import matplotlib.pyplot as plt

#Read data from CSV File
energyDataFrame = pd.read_csv('../resources/EnergyMixGeo.csv')

#Normalize data
cleanedEnergyDataFrame = energyDataFrame[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']]

#Get Countrynames
countrynames = np.array(energyDataFrame[['Country']])

#Scale Data
scaledEnergyData = pd.DataFrame(preprocessing.scale(cleanedEnergyDataFrame, axis=0, with_mean=False, with_std=True, copy=True))

# calculate distance matrix: choose the metric wisely!
distanceMatrix = pdist(scaledEnergyData, 'correlation')

# choose the cluster-linkage method
linkageData = linkage(distanceMatrix, method='average')

# draw
dendrogram(linkageData, orientation='left', labels=countrynames)
plt.show()

# cluster the countries into 4 clusters
clusterData = fcluster(linkageData, 4, criterion="maxclust")

# add the cluster-information to the cleaned data
energyDataFrame['Cluster'] = clusterData;
energyDataFrame.to_csv('../resources/EnergyMixGeoCluster.csv')

cluster1 = energyDataFrame[energyDataFrame['Cluster'] == 1]
cluster1 = cluster1[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']];
plt.subplot(411)
plt.title('Cluster 1')
plt.xticks(range(5), ('Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro'))
plt.plot(cluster1.transpose())

cluster2 = energyDataFrame[energyDataFrame['Cluster'] == 2]
cluster2 = cluster2[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']];
plt.subplot(412)
plt.title('Cluster 2')
plt.xticks(range(5), ('Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro'))
plt.plot(cluster2.transpose())

cluster3 = energyDataFrame[energyDataFrame['Cluster'] == 3]
cluster3 = cluster3[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']];
plt.subplot(413)
plt.title('Cluster 3')
plt.xticks(range(5), ('Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro'))
plt.plot(cluster3.transpose())

cluster4 = energyDataFrame[energyDataFrame['Cluster'] == 4]
cluster4 = cluster4[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']];
plt.subplot(414)
plt.title('Cluster 4')
plt.xticks(range(5), ('Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro'))
plt.plot(cluster4.transpose())

plt.subplots_adjust(left=None, bottom=None, right=None, top=None,wspace=None, hspace=0.5)
plt.show()