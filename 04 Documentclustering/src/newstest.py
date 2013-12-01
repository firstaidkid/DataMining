# -*- coding: utf-8 -*-
import feedparser as fp
import newsfeatures as nf
from newsfeatures import *
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")


print "Excercise 2.1.2"
print "Returntype of feedparser.parse()-Function:"
print str(type(fp.parse("http://feeds.reuters.com/reuters/topNews"))),"\n"

print "How to print title and description of feeds:"
print "for feed in parsedFeeds:"
print "\tfor item in feed.entries:"
print "\t\tprint item.title"
print "\t\tprint stripHTML(item.description)\n"

print "Printing titles and their descriptions:"
nf.parseFeeds()
nf.getFeedInfo()

print "#"*50,"\n"

print "Ecercise 2.2.1"
print "Create matrices"
allwords, articlewords, articletitles = getarticlewords()

print "#"*50,"\n"

print "Ecercise 2.2.2"
print "Creating Word-/Article-Matrix and Wordvector"
wordvec, wordInArt = makematrix(allwords, articlewords)

print "#"*50,"\n"

print "Ecercise 2.2.3"
print "clean matrix by deleting articles with no words from wordvec"
wordInArt, articletitles = cleanMatrix(wordInArt, articletitles)

print "#"*50,"\n"

print "Excercise 2.2.4"
print "Creating numpy matrix from word/article-matrix"
wordInArtMatrix = np.matrix(wordInArt)
print "Calling NNMF"
W, H = nnmf(wordInArtMatrix, 40, 10)

print "#"*50,"\n"

print "Excercise 2.3"
showfeatures(W, H, articletitles, wordvec)