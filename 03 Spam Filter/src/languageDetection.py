#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import feedparser
import docclass as doc
from urllib import urlopen
import nltk
from math import log10

germanBooks = ['http://www.gutenberg.org/files/19755/19755-h/19755-h.htm',
				'http://www.gutenberg.org/files/34099/34099-h/34099-h.htm',
				'http://www.gutenberg.org/files/24618/24618-h/24618-h.htm',
				'http://www.gutenberg.org/files/40714/40714-h/40714-h.htm']

englishBooks = ['http://www.gutenberg.org/files/76/76-h/76-h.htm',
				'http://www.gutenberg.org/files/1342/1342-h/1342-h.htm',
				'http://www.gutenberg.org/files/1661/1661-h/1661-h.htm',
				'http://www.gutenberg.org/files/135/135-h/135-h.htm']


clf = doc.Classifier(doc.getwords, minWordLength=3)

print '---------- Learning German Books ----------'
for book in germanBooks:
	print "Learning from: " + book
	html = urlopen(book).read()
	raw = nltk.clean_html(html)
	clf.train(raw, "DE")

print '---------- Learning English Books ----------'
for book in englishBooks:
	print "Learning from: " + book
	html = urlopen(book).read()
	raw = nltk.clean_html(html)
	clf.train(raw, "EN")

print '---------- Classifiing Text ----------'
text = '''He was still hurriedly thinking all this through, unable to decide to get out of the bed, when the clock struck quarter to seven. There was a cautious knock at the door near his head. "Gregor", somebody called - it was his mother - "it's quarter to seven. Didn't you want to go somewhere?" That gentle voice! Gregor was shocked when he heard his own voice answering, it could hardly be recognised as the voice he had had before. As if from deep inside him, there was a painful and uncontrollable squeaking mixed in with it, the words could be made out at first but then there was a sort of echo which made them unclear, leaving the hearer unsure whether he had heard properly or not. Gregor had wanted to give a full answer and explain everything, but in the circumstances contented himself with saying: "Yes, mother, yes, thank-you, I'm getting up now." The change in Gregor's voice probably could not be noticed outside through the wooden door, as his mother was satisfied with this explanation and shuffled away. But this short conversation made the other members of the family aware that Gregor, against their expectations was still at home, and soon his father came knocking at one of the side doors, gently, but with his fist. "Gregor, Gregor", he called, "what's wrong?" And after a short while he called again with a warning deepness in his voice: "Gregor! Gregor!" At the other side door his sister came plaintively: "Gregor? Aren't you well? Do you need anything?" Gregor answered to both sides: "I'm ready, now", making an effort to remove all the strangeness from his voice by enunciating very carefully and putting long pauses between each, individual word. His father went back to his breakfast, but his sister whispered: "Gregor, open the door, I beg of you." Gregor, however, had no thought of opening the door, and instead congratulated himself for his cautious habit, acquired from his travelling, of locking all doors at night even when he was at home.'''

scoreGerman = 10 * log10(clf.prob(text, "DE"))
scoreEnglish = 10 * log10(clf.prob(text, "EN"))

print "scoreGerman: " + str(scoreGerman)
print "scoreEnglish: " + str(scoreEnglish)