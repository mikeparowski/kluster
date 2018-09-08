# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
import math
from textblob import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

with open("./data/rep-platform.txt") as repf:
    rep = tb(repf.read().decode('utf-8')[:100])

with open("./data/dem-platform.txt") as demf:
    dem = tb(demf.read().decode('utf-8')[:100])

bloblist = [rep, dem]
for i, blob in enumerate(bloblist):
    print("Top words in document {}, {}".format(i + 1, repf.name if blob == rep else demf.name))
    #print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:10]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
