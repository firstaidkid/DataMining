import numpy as np
import pandas as pd
from pymaps import *

# Read data from CSV File
energyDataFrame = pd.read_csv('../resources/EnergyMixGeoCluster.csv')

# creates an icon & map by default
g = PyMap()
g.maps[0].zoom = 2

def createIconWithData (idx, name, info, long, lat, cluster):
	# specify color
	color = "black"
	if cluster == 1:
		color = "red";
	elif cluster == 2:
		color = "blue"
	elif cluster == 3:
		color = "green"
	elif cluster == 4:
		color = "yellow"
	#endif

	# create an icon
	icon = Icon('icn'+str(idx))
	icon.image = "http://labs.google.com/ridefinder/images/mm_20_"+color+".png"
	icon.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png" # do not hotlink from your web page!
	
	g.addicon(icon)
	q = [lat,long, info, 'icn'+str(idx)]	# create a marker with the defaults
	g.maps[0].setpoint(q)		# add the points to the map
    

for idx, a in energyDataFrame.iterrows():
	info =  "<h3>%s</h3><b>Oil:</b> %.1f, <b>Gas:</b> %.1f, <b>Coal:</b> %.1f, <b>Nuclear:</b> %.1f, <b>Hydro:</b> %.1f<br><b>Total 2009:</b> %.1f, <b>CO2 Emmission:</b> %.1f" % (a['Country'],a['Oil'],a['Gas'],a['Coal'],a['Nuclear'],a['Hydro'],a['Total2009'],a['CO2Emm'])
	createIconWithData(idx, a['Country'], info, a['lng'], a['lat'], a['Cluster'])

open('../results/googleMaps.htm','wb').write(g.showhtml())   # generate test file