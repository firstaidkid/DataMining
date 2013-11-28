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
		articleList = list()
		wordInArt.append(articleList)

		for word in wordvec:
			if word in article:
				articleList.append(article[word])
			else:
				articleList.append(0)

	return wordvec, wordInArt

def cleanMatrix(wordInArt, articletitles):
	for idx, article in enumerate(wordInArt):
		if sum(article) == 0:
			wordInArt.pop(idx)
			articletitles.pop(idx)
			print "Cleaned allNulls with Index: " + str(idx)

	return wordInArt, articletitles

# create matrices
allwords, articlewords, articletitles = getarticlewords()

# create Wort-/Artikel-Matrix and Wortvektor
wordvec, wordInArt = makematrix(allwords, articlewords)

# clean matrix by deleting articles with not words from wordvec
wordInArt, articletitles = cleanMatrix(wordInArt, articletitles)

# write intp data-file
fout = open("../results/wv_awm.dat", "w")
for idx, word in enumerate(wordvec):
	if idx < (len(wordvec)-1):
		fout.write(word+", ")
	else:
		fout.write(word+"\n")

for idx1, article in enumerate(wordInArt):
	for idx2, word in enumerate(article):
		if idx2 < (len(article)-1):
			fout.write(str(word)+", ")
		else:
			fout.write(str(word))
	if idx1 < (len(wordInArt)-1):
		fout.write("\n")

fout.close()


# calculates the cost/distance between to matrices
def cost(A, B):
	return np.linalg.norm(A-B)

# 2.2.4: Implementierung der NNMF
# Matrix: A, Number of Features: m, Number of Iterations: it
def nnmf(A, m, it):
	_costThreshold = 5
	r = A.shape[0]
	c = A.shape[1]

	# create array from A to have easier (element by element) matrix calculations
	_A = np.array(A)

	# check for incorrect values
	if c < m:
		return None, None

	# initially random values for "H"
	_H = np.ones((m, c))
	for i in range(0, m-1):
		for j in range(0, c-1):
			_H[i,j] = np.random.randint(0, c)

	# initially random values for "W"
	_W = np.ones((r, m))
	for i in range(0, r):
		for j in range(0, m):
			_W[i,j] = np.random.randint(0, r)

	for i in range(0, it):
		_Wt = _W.transpose()
		_Ht = _H.transpose()

		# New calculation of H
		_H = _H * ( np.dot(_Wt, _A) / np.dot(np.dot(_Wt,_W),_H) )
		# New calculation of W
		_W = _W * ( np.dot(_A, _Ht) / np.dot(np.dot(_W, _H),_Ht) )

		# Calculate Cost
		_B = _W.dot(_H)
		_cost = cost(_A,_B)

		# if cost below threshold, return factors _W and _H
		if _cost < _costThreshold:
			break

	return np.matrix(_W), np.matrix(_H)


def showfeatures(W, H, titles, wordvec):
	N = 6
	M = 3
	# TODO finish


# create numpy matrix from word/article-matrix
wordInArtMatrix = np.matrix(wordInArt)
W, H = nnmf(wordInArtMatrix, 15, 2)


