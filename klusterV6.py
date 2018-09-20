import os, random, numpy as np

from sklearn import manifold, decomposition, ensemble, discriminant_analysis, random_projection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import LocallyLinearEmbedding
import matplotlib.pyplot as plt
from pandas import DataFrame
import pickle

SOURCES = [
    #('data/articles/breitbart', 'bb'),
    #('data/articles/thinkprogress', 'tp'),
    #('data/articles/cnn', 'cnn'),
    #('data/articles/foxnews', 'fox'),
    #('data/articles/nytimes', 'nyt'),
    #('data/articles/theatlantic', 'atl'),
    #('data/articles/theblaze', 'blz'),
    #('data/articles/thefederalist', 'fed'),
    #('data/articles/vice', 'vice'),
    ('data/articles/wsj', 'wsj')
]

def plot_embedding(X, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure()
    ax = plt.subplot(111)
    for i in range(X.shape[0]):
        plt.text(X[i, 0], X[i, 1], str(digits.target[i]),
                color=plt.cm.Set1(y[i] / 10.),
                fontdict={'weight': 'bold', 'size': 9})

def build_corpus(sources):
    data = DataFrame({'text': [], 'class': []})
    for path, classification in sources:
        data = data.append(build_data_frame(path, classification))
    return data.reindex(np.random.permutation(data.index))

def build_data_frame(path, classification):
    rows = []
    index = []
    for filename, text in read_files(path):
        rows.append({'text': text, 'class': classification})
        index.append(filename)
    return DataFrame(rows, index=index)

def read_files(path):
    for article in os.listdir(path):
        with open(os.path.join(path, article)) as f:
            text = f.read()
        yield os.path.join(path, article), text

## Main
tfidf = TfidfVectorizer()
data = build_corpus(SOURCES)
X = tfidf.fit_transform(data)

rp = random_projection.SparseRandomProjection(n_components=2, random_state=42)
X_projected = rp.fit_transform(X)
plot_embedding(X_projected, "Random Projection of Docs")

