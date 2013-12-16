"""
Created on 26.02.2012

@author: maucher

This version applies cleaned data provided by matplotlib.finance

In the cleaned data also the "open" value is adjusted w.r.t. splits and dividends

"""

print __doc__


import datetime
from matplotlib import finance
import numpy as np
import pandas as pd
import sklearn.cluster as cl
from matplotlib import pyplot as plt

from sklearn import cluster
from sklearn import metrics

# Choose a time period reasonnably calm (not too long ago so that we get
# high-tech firms, and before the 2008 crash)
d1 = datetime.datetime(2003, 01, 01)
d2 = datetime.datetime(2008, 01, 01)

symbol_dict = {
        'TOT'  : 'Total',
        'XOM'  : 'Exxon',
        'CVX'  : 'Chevron',
        'COP'  : 'ConocoPhillips',
        'VLO'  : 'Valero Energy',
        'MSFT' : 'Microsoft',
        'IBM'  : 'IBM',
        'TWX'  : 'Time Warner',
        'CMCSA': 'Comcast',
        'CVC'  : 'Cablevision',
        'YHOO' : 'Yahoo',
        'DELL' : 'Dell',
        'HPQ'  : 'Hewlett-Packard',
        'AMZN' : 'Amazon',
        'TM'   : 'Toyota',
        'CAJ'  : 'Canon',
        'MTU'  : 'Mitsubishi',
        'SNE'  : 'Sony',
        'F'    : 'Ford',
        'HMC'  : 'Honda',
        'NAV'  : 'Navistar',
        'NOC'  : 'Northrop Grumman',
        'BA'   : 'Boeing',
        'KO'   : 'Coca Cola',
        'MMM'  : '3M',
        'MCD'  : 'Mc Donalds',
        'PEP'  : 'Pepsi',
        #'KFT'  : 'Kraft Foods',        # NOT WORKING
        'K'    : 'Kellogg',
        #'UN'   : 'Unilever',           # NOT WORKING
        'MAR'  : 'Marriott',
        'PG'   : 'Procter Gamble',
        'CL'   : 'Colgate-Palmolive',
        #'NWS'  : 'News Corporation',   # NOT WORKING
        'GE'   : 'General Electrics',
        'WFC'  : 'Wells Fargo',
        'JPM'  : 'JPMorgan Chase',
        'AIG'  : 'AIG',
        'AXP'  : 'American express',
        'BAC'  : 'Bank of America',
        'GS'   : 'Goldman Sachs',
        'AAPL' : 'Apple',
        'SAP'  : 'SAP',
        'CSCO' : 'Cisco',
        'TXN'  : 'Texas instruments',
        'XRX'  : 'Xerox',
        'LMT'  : 'Lookheed Martin',
        'WMT'  : 'Wal-Mart',
        'WAG'  : 'Walgreen',
        'HD'   : 'Home Depot',
        'GSK'  : 'GlaxoSmithKline',
        'PFE'  : 'Pfizer',
        'SNY'  : 'Sanofi-Aventis',
        'NVS'  : 'Novartis',
        'KMB'  : 'Kimberly-Clark',
        'R'    : 'Ryder',
        'GD'   : 'General Dynamics',
        'RTN'  : 'Raytheon',
        'CVS'  : 'CVS',
        'CAT'  : 'Caterpillar',
        'DD'   : 'DuPont de Nemours',
    }

symbols, names = np.array(symbol_dict.items()).T

print "----------------------------Symbols---------------------------------------"
print symbols

print "----------------------------Names---------------------------------------"
print names

quotes = [finance.quotes_historical_yahoo(symbol, d1, d2, asobject=True)
                for symbol in symbols]

print "----------------------------Quotes---------------------------------------"
print "Number of quotes:        ",len(quotes)


print "--------------------------open and close-----------------------------------"
#volumes = np.array([q.volume for q in quotes]).astype(np.float)
open    = np.array([q.open   for q in quotes]).astype(np.float)
close   = np.array([q.close  for q in quotes]).astype(np.float)

print "--------------------------difference-----------------------------------"
# calculate difference for all values
difference = np.diff(open - close)
print difference

print "--------------------------similiarity matrix-----------------------------------"
similiarityMatrix = np.corrcoef(difference)

# create an AffinityPropagation-Object
ap = cl.AffinityPropagation()

# fit to data
ap.fit(similiarityMatrix)

print "--------------------------plot-----------------------------------"
# create a list of dictionaries. one dictionary per cluster
plotData = [dict() for i in range(max(ap.labels_)+1)]
print plotData
for i in range(len(ap.labels_)):
    # ap.labels_[i] is the Cluster of that symbol
    # plotData[ap.labels_[i]] is a dictionary containing all symbols of that cluster
    if symbols[i] not in plotData[ap.labels_[i]]:
        plotData[ap.labels_[i]][names[i]] = pd.DataFrame(quotes[i])

# plot
for idx, cluster in enumerate(plotData):
    print "\nCluster %d:" %idx
    plt.close('all') # because MAC
    plt.figure(idx)
    for key in cluster.keys():
        print "\t%s" % key
        plt.plot(cluster[key].date, cluster[key].aclose, label=key)
    plt.figure(idx).autofmt_xdate()
    plt.legend(loc='best', fancybox=True)
    plt.show()
