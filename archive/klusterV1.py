## -*- coding: utf-8 -*-

# this is a correctly functioning tfidf for use with the two platform docs
# next steps:
## implement bigrams and trigrams correctly
## scrape for 5k articles each
## test various tfidf implementations

import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk import bigrams, trigrams
from kitchen.text.converters import getwriter
import codecs
import math
import sys

UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
stopwords = nltk.corpus.stopwords.words('english')
tokenizer = RegexpTokenizer("[\w’]+", flags=re.UNICODE)

def freq(word, doc):
    return doc.count(word)

def word_count(doc):
    return len(doc)
    #tempcount = 0
    #count = 1
    #try:
    #    for character in doc:
    #        if character == " ":
    #            tempcount += 1
    #            if tempcount == 1:
    #                count += 1
    #            else:
    #                tempcount += 1
    #        else:
    #            tempcount = 0
    #    return count
    #except:
    #    return -1

def tf(word, doc):
    return (freq(word, doc) / float(word_count(doc)))

def num_docs_containing(word, list_of_docs):
    count = 0
    for document in list_of_docs:
        if freq(word, document) > 0:
            count += 1
    return count# if count else 1

def idf(word, list_of_docs):
    return math.log(len(list_of_docs) /
            float(num_docs_containing(word, list_of_docs)))

def tf_idf(word, doc, list_of_docs):
    return (tf(word, doc) * idf(word, list_of_docs))

#Open documents
with codecs.open("./data/rep-platform.txt", encoding='utf-8', errors='ignore') as repf:
    rep = repf.read()#[:9000]
with codecs.open("./data/dem-platform.txt", encoding='utf-8', errors='ignore') as demf:
    dem = demf.read()#[:9000]

#Compute the frequency for each term.
vocabulary = []
docs = {}
docnames = {}
all_tips = []
for tip in ([rep, dem]):
    if tip == rep:
        docnames[tip] = "REPUBLICAN PLATFORM"
    else:
        docnames[tip] = "DEMOCRAT PLATFORM"
    tokens = tokenizer.tokenize(tip)

    #bi_tokens = bigrams(tokens)
    #tri_tokens = trigrams(tokens)
    tokens = [token.lower() for token in tokens if len(token) > 2]
    tokens = [token for token in tokens if token not in stopwords]

    #bi_tokens = [' '.join(token).lower() for token in bi_tokens]
    #bi_tokens = [token for token in bi_tokens if token not in stopwords]

    #tri_tokens = [' '.join(token).lower() for token in tri_tokens]
    #tri_tokens = [token for token in tri_tokens if token not in stopwords]

    final_tokens = []
    final_tokens.extend(tokens)
    #final_tokens.extend(bi_tokens)
    #final_tokens.extend(tri_tokens)
    docs[docnames[tip]] = {'freq': {}, 'tf': {}, 'idf': {},
                        'tf-idf': {}, 'tokens': []}

    for token in final_tokens:
        #The frequency computed for each tip
        docs[docnames[tip]]['freq'][token] = freq(token, final_tokens)
        #The term-frequency (Normalized Frequency)
        docs[docnames[tip]]['tf'][token] = tf(token, final_tokens)
        docs[docnames[tip]]['tokens'] = final_tokens

    vocabulary.append(final_tokens)

for doc in docs:
    for token in docs[doc]['tf']:
        #The Inverse-Document-Frequency
        docs[doc]['idf'][token] = idf(token, vocabulary)
        #The tf-idf
        docs[doc]['tf-idf'][token] = tf_idf(token, docs[doc]['tokens'], vocabulary)

#Now let's find out the most relevant words by tf-idf.
words = {}
for doc in docs:
    words[doc] = {}
    for token in docs[doc]['tf-idf']:
        if token not in words:
            words[doc][token] = docs[doc]['tf-idf'][token]
        else:
            if docs[doc]['tf-idf'][token] > words[token]:
                words[doc][token] = docs[doc]['tf-idf'][token]

    #print doc
    #for token in docs[doc]['tf-idf']:
    #    try:
    #        print "{} {}".format(token, docs[doc]['tf-idf'][token])
    #    except UnicodeEncodeError:
    #        print "unicode error in {}".format(docs[docnames[doc]])
    #        print docs[]


#print docs
print "---------------------------------------------"
print "---------------------------------------------"
print "---------------------------------------------"
print "---------------------------------------------"
#print words
for party in words:
    count = 0
    print party
    for item in sorted(words[party].items(), key=lambda x: x[1], reverse=True):
        print "%f <= %s" % (item[1], item[0])
        count += 1
        if count == 10:
            break

