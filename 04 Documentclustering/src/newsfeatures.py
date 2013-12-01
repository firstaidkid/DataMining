# -*- coding: utf-8 -*-
import feedparser as fp
from nltk.corpus import stopwords
import re
import pandas as pd
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

feedlist=["http://feeds.reuters.com/reuters/topNews","http://feeds.reuters.com/reuters/businessNews","http://feeds.reuters.com/reuters/worldNews","http://feeds2.feedburner.com/time/world","http://feeds2.feedburner.com/time/business","http://feeds2.feedburner.com/time/politics","http://rss.cnn.com/rss/edition.rss",	"http://rss.cnn.com/rss/edition_world.rss","http://newsrss.bbc.co.uk/rss/newsonline_world_edition/business/rss.xml","http://newsrss.bbc.co.uk/rss/newsonline_world_edition/europe/rss.xml","http://www.nytimes.com/services/xml/rss/nyt/World.xml","http://www.nytimes.com/services/xml/rss/nyt/Economy.xml"]
parsedFeeds = list()

def parseFeeds(showParsing=False):
	for feed in feedlist:
		if showParsing == True:
			print "Parsing feed: ",str(feed)
		parsedFeeds.append(fp.parse(feed))

def getFeedInfo():
	for feed in parsedFeeds:
		for item in feed.entries:
			print "Title:"
			print item.title
			print "Description:"
			print stripHTML(item.description)
			print "-"*60

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
			#print "Cleaned allNulls with Index: " + str(idx)

	return wordInArt, articletitles

# create matrices
allwords, articlewords, articletitles = getarticlewords()

# create Word-/Article-Matrix and Wordvector
wordvec, wordInArt = makematrix(allwords, articlewords)

# clean matrix by deleting articles with no words from wordvec
wordInArt, articletitles = cleanMatrix(wordInArt, articletitles)

# write into data-file
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

# 2.2.4: Implementation of NNMF
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
		print "Cost:", _cost

		# if cost below threshold, return factors _W and _H
		if _cost < _costThreshold:
			break

	return np.matrix(_W), np.matrix(_H)


def showfeatures(W, H, titles, wordvec):
	N = 6
	M = 3
	subject = list()

	# Aufgabe 2.3.1
	print "-"*150
	print "Printing the most relevant words for each feature"
	print "-"*150
	for i in range(H.shape[0]):
		# create a list for every feature H
		featureList = list()
		for j in range(H.shape[1]):
			# append weight of element H[i,j] and j-th word of the wordvec to the list
			featureList.append([H[i,j], wordvec[j]])
		# reverse sort the featureList, to get the most relevant words on top
		featureList.sort()
		featureList.reverse()

		# print the N=6 most relevant words for a feature to the console
		featuresWords = ""
		print "The "+str(N)+" most relevant words for feature "+str(i)+ ":" 
		# go through featureList
		for k in featureList[0:N]:
			# create string of all feature words that belong together
			featuresWords = featuresWords + " " + str(k[1])
			# print the single words and their weight property
			print str(k[0])+" "*(20-len(str(k[0])))+str(k[1])

		# create a list of all words that describe a feature
		subject.append(featuresWords)


	print "-"*150
	print "Printing the most relevant features for each article"
	print "-"*150
	# Aufgabe 2.3.2
	# print the M=3 most relevant features for an article to the console
	for i in range(W.shape[0]):
		# create a list for every article in W
		relevanceList = list()
		for j in range(W.shape[1]):
			# append weight of feature at W[i,j] and its subject to the list
			relevanceList.append([W[i,j],subject[j]])
		# reverse sort the relevanceList, to get the most relevant subjects on top
		relevanceList.sort()
		relevanceList.reverse()

		# print everything out to the console
		print "Article "+str(i)+": \""+titles[i]+"\""
		for item in relevanceList[0:M]:
			print str(item[0]) +" "*(20-len(str(item[0]))) + str(item[1])

	print "-"*150
	print "Printing the most relevant articles for each feature"
	print "-"*150
	# print the M=3 most relevant articles for a feature to the console
	for i in range(W.shape[1]):
		# create a list for every posible feature of an article
		bestArticleForFeature = list()
		for j in range(W.shape[0]):
			# append the weight of W[j,i] and the articles title to the list
			bestArticleForFeature.append([W[j, i], titles[j]])
		# reverse sort the bestArticleForFeature-list, to get the most relevant articles on top
		bestArticleForFeature.sort()
		bestArticleForFeature.reverse()

		# print the subject and the M=3 articles with their corresponding weight to the console
		print "Feature "+str(i)+": \"" + subject[i] +"\"" 
		for features in bestArticleForFeature[0:M]:
			print str(features[0]) + " "*(20-len(str(features[0]))) + str(features[1])

	



# create numpy matrix from word/article-matrix
<<<<<<< HEAD
# wordInArtMatrix = np.matrix(wordInArt)
# W, H = nnmf(wordInArtMatrix, 40, 10)
# showfeatures(W, H, articletitles, wordvec)
=======
wordInArtMatrix = np.matrix(wordInArt)

print "-"*150
print "Calculating NNMF"
print "-"*150
W, H = nnmf(wordInArtMatrix, 40, 10)

print "-"*150
print "Calculating ShowFeatures"
print "-"*150
showfeatures(W, H, articletitles, wordvec)
>>>>>>> 47304a035207c81524e43e92b4fead6cb581f77a


