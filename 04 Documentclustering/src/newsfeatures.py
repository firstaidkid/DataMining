import feedparser as fp
from nltk.corpus import stopwords
import re
import pandas as pd
import numpy as np

feedlist=["http://feeds.reuters.com/reuters/topNews","http://feeds.reuters.com/reuters/businessNews","http://feeds.reuters.com/reuters/worldNews","http://feeds2.feedburner.com/time/world","http://feeds2.feedburner.com/time/business","http://feeds2.feedburner.com/time/politics","http://rss.cnn.com/rss/edition.rss",	"http://rss.cnn.com/rss/edition_world.rss","http://newsrss.bbc.co.uk/rss/newsonline_world_edition/business/rss.xml","http://newsrss.bbc.co.uk/rss/newsonline_world_edition/europe/rss.xml","http://www.nytimes.com/services/xml/rss/nyt/World.xml","http://www.nytimes.com/services/xml/rss/nyt/Economy.xml"]

parsedFeeds = list()
for feed in feedlist:
	parsedFeeds.append(fp.parse(feed))

# for feed in parsedFeeds:
# 	for item in feed.entries:
# 		print item.title
# 		print item.description

def stripHTML(h):
	p=""
	s=0
	for c in h:
		if c=="<": s=1
		elif c==">":
			s=0
			p+=" "
		elif s==0:
			p+=c
	return p

sw = stopwords.words("english")
def seperatewords(text):
	splitter = re.compile("\\W*")
	return [s.lower() for s in splitter.split(text) if len(s)>4 and s not in sw]

def getarticlewords():
	#initialize return datastructures
	allwords = dict()
	articlewords = list()
	articletitles = list()

	# go through all parsed feeds
	for feed in parsedFeeds:
		# get all articles in the feed
		for item in feed.entries:
			# add the articles title to the articletitles list
			articletitles.append(item.title)
			# clean out all markup form the articles description and save it in one string with the title
			itemString = item.title +" "+ stripHTML(item.description)
			# sepereate all words
			itemWordList = seperatewords(itemString)
			# generate new dictionary in articlewords list for every article
			articlewords.append(dict())
			# iterate through all words in itemWordList
			for word in itemWordList:
				# initialize value for key 'word' in allwords dict with 0
				if word not in allwords:
					allwords[word] = 0
				# initialize value for key 'word' in articlewords list with 0
				if word not in articlewords[len(articlewords)-1]:
					articlewords[len(articlewords)-1][word] = 0

				# increment count of appearance for word in articlewords list
				articlewords[len(articlewords)-1][word] += 1
				# increment count of appearance for word in allwords dict				
				allwords[word] += 1

	return allwords, articlewords, articletitles

def makematrix(allw, articlew):
	wordvec = list()
	wordInArt = list()

	for word in allw:
		articleCount = 0.0
		if allw[word] < 4:
			continue
		for article in articlew:
			if word not in article:
				continue
			articleCount += 1

		#print word +";" +str(articleCount)+";"+str(len(articlew))
		#print str(articleCount/len(articlew))
		if articleCount/len(articlew) < 0.6:
			wordvec.append(word)

	for article in articlew:
		allNulls = True
		articleList = list()
		wordInArt.append(articleList)

		for word in wordvec:
			if word in article:
				articleList.append(article[word])
				allNulls = False
			else:
				articleList.append(0)

		# if an article would be all-Nulls, delete it from the lists
		if allNulls:
			print "Found an allNull."
			wordInArt.pop()

	return wordvec, wordInArt

articleWords = getarticlewords()
matrix = makematrix(articleWords[0],articleWords[1])

#print matrix[0]
#print "#"*158
fout = open("../results/wv_awm.dat", "w")
for idx, word in enumerate(matrix[0]):
	if idx < (len(matrix[0])-1):
		fout.write(word+", ")
	else:
		fout.write(word+"\n")

for idx1, article in enumerate(matrix[1]):
	for idx2, word in enumerate(article):
		if idx2 < (len(article)-1):
			fout.write(str(word)+", ")
		else:
			fout.write(str(word))
	if idx1 < (len(matrix[1])-1):
		fout.write("\n")

fout.close()

# create numpy array from word/article-matrix
npMatrix = np.matrix(matrix[1])

# calculates the cost/distance between to matrices
def cost(A, B):
	return np.linalg.norm(A-B)

# Matrix: A, Number of Features: m, Number of Iterations: it
def nnmf(A, m, it):
	_costThreshold = 5

	# check for incorrect values
	if len(A) < m:
		return None, None

	# initially random values for "H"
	_H = np.zeros((m,len(A)))
	_W = np.zeros((A.shape[0], m))


	for i in range(0, it):
		#CORRECT HERE
		# New calculation of H
		_H = np.array(_H) * np.array( (np.array(_W.transpose())*np.array(A)) / (np.array(_W.transpose()) * np.array(_W) * np.array(_H)) )
		# New calculation of W
		_W = np.array(_W) * np.array( (np.array(A) * np.array(_H.transpose())) / np.array(np.array(_W) * np.array(_H) * np.array(_H.transpose())) )

		# Calculate Cost
		_B = np.array(_W) * np.array(_H)
		_cost = cost(A,_B)
		print _cost

		# if cost below threshold, return A
		if _cost < _costThreshold:
			return _W, _H

	return _W, _H



print nnmf(npMatrix, 15, 2)

