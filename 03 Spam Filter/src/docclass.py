#imports
import re


def getwords(doc):
	words = doc.split()
	print words
	cleanedWords= [t.strip("().,:;!?-").lower() for t in words]
	print cleanedWords

getwords("Hello World. Today is a beautiful monday morning (the 18th of November).")

