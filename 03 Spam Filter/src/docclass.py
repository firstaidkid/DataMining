#imports

def getwords(doc, minWordLength = 3, maxWordLength = 20):
	words = doc.split()
	print words
	cleanedWords= [t.strip("().,:;!?-").lower() for t in words if (len(t) > minWordLength) and (len(t) < maxWordLength)]
	print cleanedWords

getwords("Hello World. Today is a beautiful monday morning (the 18th of November). dieseswortistvielzulangsagichdir")

