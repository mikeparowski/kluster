import os, sys, random, numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sklearn.cluster import SpectralClustering, KMeans
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from pandas import DataFrame
from pprint import pprint

SOURCES = [
    #('data/articles/test0', 't0'),
    #('data/articles/test1', 't1'),
    ('data/articles/breitbart', 'bb'),
    ('data/articles/thinkprogress', 'tp'),
    #('data/articles/cnn', 'cnn'),
    #('data/articles/foxnews', 'fox'),
    #('data/articles/nytimes', 'nyt'),
    #('data/articles/theatlantic', 'atl'),
    #('data/articles/theblaze', 'blz'),
    #('data/articles/thefederalist', 'fed'),
    #('data/articles/vice', 'vice'),
    #('data/articles/wsj', 'wsj')
]

ext_map = {
    'bb': 1,
    'tp': 2,
    'cnn': 2,
    'fox': 3,
    'nyt': 4,
    'atl': 5,
    'blz': 6,
    'fed': 7,
    'vice': 8,
    'wsj': 9,
    't0': 10,
    't1': 11
}

quant_map = {
        'bb': 5000,#1000,
        'tp': 5000,#100,#1000,
        't0': 1,
        't1': 1,
        'cnn': 50,#50,#500,
        'fox': 50,#50,#500,
        'nyt': 50,#25,#250,
        'wsj': 500,#25,#250,
        'atl': 50,#5,#50,
        'blz': 50,#5,#50,
        'fed': 50,#5,#50,
        'vice': 50,#5#50
}

def build_corpus(sources):
    data = DataFrame({'text': [], 'class': []})
    for path, classification in sources:
        data = data.append(build_data_frame(path, classification))
    return data.reindex(np.random.permutation(data.index))

def build_data_frame(path, classification):
    rows = []
    index = []
    for filename, text in read_files(path, classification):
        rows.append({'text': text, 'class': ext_map[classification]})
        index.append(filename[:30])
    return DataFrame(rows, index=index)

def read_files(path, classification):
    nfiles = quant_map[classification]
    listdir = os.listdir(path)
    random.shuffle(listdir)
    for article in listdir[:nfiles]:
        with open(os.path.join(path, article)) as f:
            text = f.read()
        yield article, text

def find_similar(tfidf_matrix, index, top_n = 5):
    cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
    return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]

#n_clusters=2
#tfidf = TfidfVectorizer(max_df=0.8, min_df=0.2,ngram_range=(1,3),norm='l2')
#data = build_corpus(SOURCES)
#X = tfidf.fit_transform(data['text'])
#dist = 1 - linear_kernel(X)
#print(X.shape)
#print(tfidf.get_feature_names())
#print(dist)
