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
print "\n %s \n\n" % (str(recommendations))

#2.4 Berechnung von Empfehlungen mit ICF
def transformCritics(critics):
	# create a new dictionary
	films = dict()
	# iterate over critics
	for critic in critics:
		# iterate over films of that critic
		for film in critics[critic]:
			# check if film is already in films dictionary
			if film not in films:
				# if not, create new entry
				films[film] = dict()
			#endif
			# add critic and his rating to that film
			films[film][critic]=critics[critic][film]
		#endfor
	# endfor
	return films


transCritics = transformCritics(rm.critics)

def calculateSimilarItems(prefs, similarity):
	# create new dictionary for similarities
	simFilms = dict()
	# iterate over films
	for film in prefs:
		# calculate correlations for each film and save them to dictionary
		simFilms[film] = topMatches(prefs, film, similarity)
	#endfor
	return simFilms


def getRecommendedItems(prefs, person, similarity):
	notRatedFilms = dict()
	ratedFilms = dict()
	similarItems = calculateSimilarItems(prefs, similarity)
	# iterate through all films
	for film in prefs:
		# filter not rated films
		if person not in prefs[film]:
			notRatedFilms[film] = similarItems[film]
		else:
			ratedFilms[film] = prefs[film][person]

	_sum = dict()
	_sumSim = dict()
	# go through all not rated films
	for notRatedFilm in notRatedFilms:
		if notRatedFilm not in _sum:
			_sum[notRatedFilm] = 0
			_sumSim[notRatedFilm] = 0
		# get rated films
		for ratedFilm in ratedFilms:
			# do not trust films with negative pearson similarities!
			if similarity == rm.sim_pearson and  similarItems[notRatedFilm]["Similarity"][ratedFilm] <= 0:
				continue
			# add up the products of rating and similarity
			_sum[notRatedFilm] +=ratedFilms[ratedFilm]*notRatedFilms[notRatedFilm]['Similarity'][ratedFilm]
			# add up similarities
			_sumSim[notRatedFilm] += notRatedFilms[notRatedFilm]['Similarity'][ratedFilm]

	# normalize results
	for film in _sum:
		if _sumSim[film] == 0:
			continue
		_sum[film] /= _sumSim[film]

	# sort results
	df = pd.DataFrame(_sum, index=["Normalized"]).transpose();
	return df.sort(columns=["Normalized"], ascending=False)


print "getRecommendedItems(EUCLID)"
print getRecommendedItems(transCritics,"Toby",rm.sim_euclid)

print "\ngetRecommendedItems(PEARSON)"
print getRecommendedItems(transCritics,"Toby",rm.sim_pearson)

