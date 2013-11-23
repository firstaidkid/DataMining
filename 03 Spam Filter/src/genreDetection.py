#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import feedparser
import docclass as doc
from urllib import urlopen

adventureBooks = ['http://www.gutenberg.org/cache/epub/78/pg78.txt',
				'http://www.gutenberg.org/cache/epub/2166/pg2166.txt',
				'http://www.gutenberg.org/cache/epub/10551/pg10551.txt',
				'http://www.gutenberg.org/cache/epub/558/pg558.txt']

medicineBooks = ['http://www.gutenberg.org/cache/epub/24564/pg24564.txt',
				'http://www.gutenberg.org/cache/epub/13397/pg13397.txt',
				'http://www.gutenberg.org/cache/epub/12036/pg12036.txt',
				'http://www.gutenberg.org/cache/epub/747/pg747.txt']


clf = doc.Classifier(doc.getwords, minWordLength=3)

print '---------- Learning Adventure Books ----------'
for book in adventureBooks:
	print "Learning from: " + book
	text = urlopen(book).read()
	clf.train(text, "Adventure")

print '---------- Learning Medicine Books ----------'
for book in medicineBooks:
	print "Learning from: " + book
	text = urlopen(book).read()
	clf.train(text, "Medicine")

print '---------- Classifiing Text ----------'
text = '''
Phileas Fogg was not known to have either wife or children, which may
happen to the most honest people; either relatives or near friends,
which is certainly more unusual.  He lived alone in his house in
Saville Row, whither none penetrated.  A single domestic sufficed to
serve him.  He breakfasted and dined at the club, at hours
mathematically fixed, in the same room, at the same table, never taking
his meals with other members, much less bringing a guest with him; and
went home at exactly midnight, only to retire at once to bed.  He never
used the cosy chambers which the Reform provides for its favoured
members.  He passed ten hours out of the twenty-four in Saville Row,
either in sleeping or making his toilet.  When he chose to take a walk
it was with a regular step in the entrance hall with its mosaic
flooring, or in the circular gallery with its dome supported by twenty
red porphyry Ionic columns, and illumined by blue painted windows.
When he breakfasted or dined all the resources of the club--its
kitchens and pantries, its buttery and dairy--aided to crowd his table
with their most succulent stores; he was served by the gravest waiters,
in dress coats, and shoes with swan-skin soles, who proffered the
viands in special porcelain, and on the finest linen; club decanters,
of a lost mould, contained his sherry, his port, and his
cinnamon-spiced claret; while his beverages were refreshingly cooled
with ice, brought at great cost from the American lakes.'''

scoreAdenture = clf.prob(text, "Adventure")
scoreMedicine = clf.prob(text, "Medicine")

print "scoreAdenture: " + str(scoreAdenture)
print "scoreMedicine: " + str(scoreMedicine)