from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from nltk import bigrams, trigrams
from nltk.corpus import stopwords
import re, string, os, sys, math

def build_dictionary(directory):
    vocab = []
    for art in os.listdir(directory):
        article = os.path.join(directory, art)
        with open(article) as f:
            article = f.read()
        aritcle = re.sub(r'[^\x00-\x7F]+', ' ', article)
        article = clean_text(article)
        vocab += article
    return list(set(vocab))


## Main
breitbart = './data/breitbart/'
thinkprogress = './data/thinkprogress/'

## open testfile and clean
with open('./data/breitbart/little_house_on_the_prairie_st.bb') as f:
    article = f.read()

print "building vocab..."
## build vocab
vocabulary = list(set(build_dictionary(breitbart)
    + build_dictionary(thinkprogress)
    + tokens))
print "done"

print "storing corpus..."
# store corpus
docs = []
for i in os.listdir(breitbart):
    docs.append(os.path.join('./data/breitbart/', i))
for i in os.listdir(thinkprogress):
    docs.append(os.path.join('./data/thinkprogress/', i))
print "done"

print "calculating tf..."
worddict = {}
length = len(tokens)
# calculate tf
for entry in vocabulary:
    if entry in worddict:
        continue
    tf = tokens.count(entry) / float(length)
    worddict[entry] = tf
print "done"
print "calculating tfidf..."
# calculate tfidf
for word in worddict:
    if worddict[word] == 0: continue
    count = 0
    for doc in docs:
        tokens = clean_file(doc)
        if tokens.count(word) > 0:
            count += 1
    idf = math.log(len(docs) / float(count))
    worddict[word] *= idf
print "done"


sorted_tf = [ (score, word) for word, score in worddict.iteritems() ]
sorted_tf.sort(reverse=True)
for score, word in sorted_tf:
    print "{}: {}".format(word, score)

## calculates correct tf, now loop through all (or just tp?) docs and count occurrences for idf
#tokens, bigrams = clean_text(article)
#bigrams = [' '.join(token) for token in bigrams]
#print tokens, bigrams
