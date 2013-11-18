#imports

# Exercise 2.1.1
def getwords(doc, minWordLength = 2, maxWordLength = 20):
	# split input string by whitespace
	words = doc.split()
	# delete punctuation mark and ignore words of min- and max length
	cleanedWords= [t.strip("().,:;!?-").lower() for t in words if (len(t) > minWordLength) and (len(t) < maxWordLength)]
	# fill Dictionary --> key: word value: 1
	wordDict = {key:1 for key in cleanedWords}
	return wordDict

getwords("Hello World. Today is a beautiful monday morning (the 18th of November). dieseswortistvielzulangsagichdir")

# Exercise 2.1.2
class Classifier:
	def __init__(self, getfeatures):
		self.fc = dict()
		self.cc = dict()
		self.initprob = 1.0
		self.getfeatures = getfeatures

	# increases fc-count for given word and category
	def  incf(self, f, cat):
		# test if word is already in dictionary, if not create entry
		if f not in self.fc:
			self.fc[f] = dict()

		# test if word has been categorized for cat
		if cat not in self.fc[f]:
			self.fc[f][cat] = 0

		# increment
		self.fc[f][cat] += 1

	# increases cc-count for category
	def  incc(self, cat):
		# test if category already exists, otherwise initialize with zero
		if cat not in self.cc:
			self.cc[cat] = 0
			# the initial probability is equal amongst all document categories
			self.initprob = 1.0/len(self.cc)
		self.cc[cat] += 1

	# returns the frequency of a word in a category 
	def fcount(self, f, cat):

		# test if word is already in dictionary, if not return zero
		if f not in self.fc:
			#print "word " +str(f) + " not found." 
			return 0

		# test if word has been categorized for cat, if not return zero
		if cat not in self.fc[f]:
			#print "cat " +str(cat) + " not found for word "+str(f)+"." 
			return 0
		
		return self.fc[f][cat] 

	# returns the number how ofter a word is in all documents
	def count(self, f):
		if f not in self.fc:
			return 0
		return sum(self.fc[f].values())

	# return the number of documents in a category
	def catcount(self, cat):
		# test if category already exists, otherwise throw exception
		if cat not in self.cc:
			raise NameError("ERROR: No Documents for Category: " +str(cat)+ ".")
		return self.cc[cat]

	# return total number of documents
	def totalcount(self):
		return sum(self.cc.values())

	# takes a text and the corresponding category and trains the classifier
	def train(self, item, cat):
		# get features
		features = self.getfeatures(item)
		
		# increment category count for each word
		for key in features:
			self.incf(key, cat)

		# increment document count for categories
		self.incc(cat)

	# calculates P(f|cat)
	def fprob(self, f, cat):
		return float(self.fcount(f,cat))/float(self.catcount(cat))

	# calculates smoothed P(f|cat)
	def weightedprob(self, f, cat):
		return (self.initprob + self.count(f) * self.fprob(f, cat))/(1+self.count(f))

	# return probability for item being of category cat
	def prob(self, item, cat):
		features = self.getfeatures(item)
		probs = 1.0
		for f in features:
			probs *= self.weightedprob(f,cat)

		# divide P(f|cat) through a-priori of cat
		return probs * self.catcount(cat)/self.totalcount()



clf = Classifier(getwords)
clf.train("nobody owns the water", "G")
clf.train("the quick rabbit jumps fences", "G")
clf.train("buy pharmaceuticals now", "B")
clf.train("make quick money at the online casino", "B")
clf.train("the quick brown fox jumps", "G")
clf.train("next meeting is at night", "G")
clf.train("meeting with your superstar", "B")
clf.train("money like water", "B")

item = "the money jumps"
good = clf.prob(item,"G")
bad = clf.prob(item,"B")

pgood = good/(good+bad)
pbad = bad/(good+bad)

print "GOOD: " + str(pgood)
print "BAD: " + str(pbad)
print "Result: " + max({"G": pgood, "B": pbad})





