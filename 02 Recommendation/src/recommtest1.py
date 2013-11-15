import recommendations as rm
import numpy as np
import pandas as pd


#2.2 Ahnlichkeitsbestimmung
def topMatches(prefs,person,similarity):
	results = dict()
	# iterate through all keys
	for critic in prefs:
		# ignore the person to check against
		if critic != person:
			# set normed true for euclid only
			if similarity == rm.sim_euclid:
				results[critic] = similarity(prefs, person, critic, normed=True)
			else:
				results[critic] = similarity(prefs, person, critic)
			#endif
		#endif
	#endfor

	# save into dataframe
	df = pd.DataFrame(results, index=["Similarity"]);

	# transpose and sort
	return df.transpose().sort(columns=["Similarity"], ascending=False)

# calculate matches for both functions
result_euclid = topMatches(rm.critics, "Toby", rm.sim_euclid)
result_pearson = topMatches(rm.critics, "Toby", rm.sim_pearson)

print "Euclid:\n%s \n\nPearson:\n%s" % (str(result_euclid), str(result_pearson))


#2.3 Berechnung von Empfehlungen mit User basiertem Collaborative Filtering
def getRecommendations(prefs,person,similarity):
	_correlations = topMatches(prefs,person,similarity)
	_sum = dict()
	_sumCorrelations = dict()
	#find films which person did not watch
	for critic in prefs:
		if critic != person:
			# critic has negative correlation, ignore him
			if _correlations.at[critic, "Similarity"] < 0:
				continue

			# go through all films of that critic
			for film in prefs[critic]:
				# if person has not rated the film yet
				if film not in prefs[person]:
					# add the movie to the possible moview of not in yet
					if film not in _sum:
						_sum[film] = 0.0
						_sumCorrelations[film] = 0
					#endif

					# add the new review-value to the film-value
					_sum[film] += prefs[critic][film] * _correlations.at[critic, "Similarity"]

					# add correlation of the person to kSum
					_sumCorrelations[film] += _correlations.at[critic, "Similarity"]
				#endif
			#endfor
		#endif
	#endfor

	# divide the sum by the summed correlations to get the kSum
	_kSum = dict()
	for film in _sum:
		_kSum[film] = _sum[film] / _sumCorrelations[film]

	# save into dataframe and transpose
	df = pd.DataFrame(_kSum, index=["kSum"]).transpose();

	# sort and return
	return df.sort(columns=["kSum"], ascending=False)

recommendations = getRecommendations(rm.critics, "Toby", rm.sim_euclid)
print "\n %s" % (str(recommendations))