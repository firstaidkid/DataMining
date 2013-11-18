#imports
import re


def getwords(doc):
	wordDict = dict()
	words = doc.split()
	print words
	cleanedWords= [t.strip("().,:;!?-").lower() for t in words if (len(t) > 3) and (len(t) <20)]
	print cleanedWords


getwords("Hello World. Today is a beautiful monday morning (the 18th of November).")

