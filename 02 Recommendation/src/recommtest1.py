import recommendations as rm
import numpy as np
import pandas as pd


def topMatches(prefs,person,similarity):
	results = dict()
	# iterate through all keys
	for critic in prefs:
		if critic != person:
			if similarity == rm.sim_euclid:
				results[critic] = similarity(prefs, person, critic, normed=True)
			else:
				results[critic] = similarity(prefs, person, critic)

	# save into dataframe
	df = pd.DataFrame(results, index=["Similarity"]);

	# transpose and sort
	return df.transpose().sort(columns=["Similarity"], ascending=False)


result_euclid = topMatches(rm.critics, 'Toby', rm.sim_euclid)
result_pearson = topMatches(rm.critics, 'Toby', rm.sim_pearson)

print "Euclid:\n%s \n\nPearson:\n%s" % (str(result_euclid), str(result_pearson))