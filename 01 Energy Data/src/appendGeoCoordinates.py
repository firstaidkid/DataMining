import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib, json, csv
import time

def geocode(addr):
	url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" %   (urllib.quote(addr.replace(' ', '+')))
	data = urllib.urlopen(url).read()
	#print json.loads(data).get("status") == "OVER_QUERY_LIMIT"
	
	# if we exceeded our request limit, wait for 0.5 seconds and try again
	if json.loads(data).get("status") == "OVER_QUERY_LIMIT":
		time.sleep(0.5)
		return (geocode(addr))
	info = json.loads(data).get("results")[0].get("geometry").get("location")
	return info

# Read data
data = pd.read_csv("../resources/EnergyMix.csv")

# Add columns for lat and long to dataframe
data['lat'] = pd.Series(0., index=data.index)
data['lng'] = pd.Series(0., index=data.index)

# Access GoogleMaps
#Loop to feed the func with adresses and output the lat & lng.
i = 0
print "Fetching Geocoordinates"
for country in data['Country']:
	r = geocode(country)
	data.at[i,'lat'] = r['lat']
	data.at[i,'lng'] = r['lng']
	i = i+1
	print "%s: %s %s" % (country, r['lat'], r['lng'])

# save to file
data.to_csv('../resources/EnergyMixGeo.csv')

# Plot and show
plt.xlabel('Countries')
plt.subplot(511)
plt.title('Oil')
plt.xticks(np.arange(len(data)), data['Country'])
plt.stem(data['Oil'], linefmt='k-', markerfmt='ko')

plt.subplot(512)
plt.title('Gas')
plt.xticks(np.arange(len(data)), data['Country'])
plt.stem(data['Gas'], linefmt='r-', markerfmt='ro')

plt.subplot(513)
plt.title('Coal')
plt.xticks(np.arange(len(data)), data['Country'])
plt.stem(data['Coal'], linefmt='g-', markerfmt='go')

plt.subplot(514)
plt.title('Nuclear')
plt.xticks(np.arange(len(data)), data['Country'])
plt.stem(data['Nuclear'], linefmt='y-', markerfmt='yo')

plt.subplot(515)
plt.title('Hydro')
plt.xticks(np.arange(len(data)), data['Country'])
plt.stem(data['Hydro'], linefmt='b-', markerfmt='bo')
plt.subplots_adjust(left=None, bottom=None, right=None, top=None,wspace=None, hspace=0.5)
plt.show()