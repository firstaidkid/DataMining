import numpy as np
import pandas as pd
from pymaps import *

# Read data from CSV File
energyDataFrame = pd.read_csv('../resources/EnergyMixGeoCluster.csv')
numKeys = len(energyDataFrame);

# creates an icon & map by default
g = PyMap()
g.maps[0].zoom = 2
g.key = "ABQIAAAAQQRAsOk3uqvy3Hwwo4CclBTrVPfEE8Ms0qPwyRfPn-DOTlpaLBTvTHRCdf2V6KbzW7PZFYLT8wFD0A" # you will get your own key


def createIconWithData (id, name, info, long, lat, cluster):
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
	icon = Icon(name)
	icon.image = "http://labs.google.com/ridefinder/images/mm_20_"+color+".png"
	icon.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png" # do not hotlink from your web page!
	
	g.addicon(icon)
	q = [long,lat, info, name]	# create a marker with the defaults
	g.maps[id].setpoint(q)		# add the points to the map
    

numIcons = 0
for a in energyDataFrame.itertuples(index=False):
	info =  "<h3>%s</h3><b>Oil:</b> %.1f, <b>Gas:</b> %.1f, <b>Coal:</b> %.1f, <b>Nuclear:</b> %.1f, <b>Hydro:</b> %.1f<br><b>Total 2009:</b> %.1f, <b>CO2 Emmission:</b> %.1f" % (a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9])
	createIconWithData(numIcons, a[2], info, a[10], a[11], a[12])

open('../results/googleMaps.htm','wb').write(g.showhtml())   # generate test file