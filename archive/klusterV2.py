## -*- coding: utf-8 -*-

# in order for this to effectively separate "rep" and "dem" docs, 
# tf must be calculated within its own corpus first, then combined
# w/ the idf in all docs of the opposite corpus

# tf of a word in 1 document with the idf of all opposite docs
# tf of a word in all rep docs with idf of all dem docs
# could do multiple experiments:
# do full tf-idf with just rep docs and just dem docs, then do combined to see what's most important to each party that isn't to the other
# tf with rep doc and idf with all dem docs

# bigrams and trigrams need their own tf-idfs, freq can't be trigram/all single words

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


def fill_tf(docs, tip, docnames, tokens_list):
    for token in tokens_list:
        #The frequency computed for each tip
        docs[docnames[tip]]['freq'][token] = freq(token, tokens_list)
        #The term-frequency (Normalized Frequency)
        docs[docnames[tip]]['tf'][token] = tf(token, tokens_list)
        docs[docnames[tip]]['tokens'] = tokens_list

    return tokens_list


def freq(word, doc):
    return doc.count(word)


def word_count(doc):
    return len(doc)


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
    rep = repf.read()#[:2000]
with codecs.open("./data/dem-platform.txt", encoding='utf-8', errors='ignore') as demf:
    dem = demf.read()#[:2000]


#Compute the frequency for each term.
#vocabulary = []
vocab = []
bi_vocab = []
tri_vocab = []
docs = {}
docnames = {}
for tip in ([rep, dem]):
    if tip == rep:
        docnames[tip] = "REPUBLICAN PLATFORM"
    else:
        docnames[tip] = "DEMOCRAT PLATFORM"

    tokens = tokenizer.tokenize(tip)
    bi_tokens = bigrams(tokens)
    tri_tokens = trigrams(tokens)

    tokens = [token.lower() for token in tokens if len(token) > 2]
    tokens = [token for token in tokens if token not in stopwords]

    bi_tokens = [' '.join(token).lower() for token in bi_tokens]
    bi_tokens = [token for token in bi_tokens if token not in stopwords]

    tri_tokens = [' '.join(token).lower() for token in tri_tokens]
    tri_tokens = [token for token in tri_tokens if token not in stopwords]

    docs[docnames[tip]] = {'freq': {}, 'tf': {}, 'idf': {},
                        'tf-idf': {}, 'tokens': []}

    vocab.append(fill_tf(docs, tip, docnames, tokens))
    bi_vocab.append(fill_tf(docs, tip, docnames, bi_tokens))
    tri_vocab.append(fill_tf(docs, tip, docnames, tri_tokens))

for doc in docs:
    for token in docs[doc]['tf']:
        if len(token.split(" ")) == 1:
            #The Inverse-Document-Frequency
            docs[doc]['idf'][token] = idf(token, vocab)
            #The tf-idf
            docs[doc]['tf-idf'][token] = tf_idf(token, docs[doc]['tokens'], vocab)
        elif len(token.split(" ")) == 2:
            #The Inverse-Document-Frequency
            docs[doc]['idf'][token] = idf(token, bi_vocab)
            #The tf-idf
            docs[doc]['tf-idf'][token] = tf_idf(token, docs[doc]['tokens'], bi_vocab)
        elif len(token.split(" ")) == 3:
            #The Inverse-Document-Frequency
            docs[doc]['idf'][token] = idf(token, tri_vocab)
            #The tf-idf
            docs[doc]['tf-idf'][token] = tf_idf(token, docs[doc]['tokens'], tri_vocab)


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

#print docs
print "---------------------------------------------"
print "---------------------------------------------"
print "---------------------------------------------"
print "---------------------------------------------"
#print words
for party in words:
    #count = 0
    print party
    for item in sorted(words[party].items(), key=lambda x: x[1], reverse=True):
        print "%f <= %s" % (item[1], item[0])
        #count += 1
        #if count == 50:
        #    break

