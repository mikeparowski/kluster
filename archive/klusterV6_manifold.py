## There's some promise here, especially with Spectral Embedding, 
## so probably should figure out what that is at some point. In
## the meantime, going to focus on simpler clustering methods
## until I have a firmer (more firm?) grasp on this. Just seems
## like I'm not quite there for ndr.
import os, sys, pickle, random, warnings, numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD, LatentDirichletAllocation
from sklearn import manifold, random_projection, preprocessing
from sklearn.metrics.pairwise import linear_kernel
from matplotlib.ticker import NullFormatter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pandas import DataFrame
from time import time

Axes3D
warnings.simplefilter("ignore")

SOURCES = [
    ('data/articles/breitbart', 'bb'),
    ('data/articles/thinkprogress', 'tp'),
    ('data/articles/cnn', 'cnn'),
    ('data/articles/foxnews', 'fox'),
    ('data/articles/nytimes', 'nyt'),
    ('data/articles/theatlantic', 'atl'),
    ('data/articles/theblaze', 'blz'),
    ('data/articles/thefederalist', 'fed'),
    ('data/articles/vice', 'vice'),
    ('data/articles/wsj', 'wsj')
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
    'wsj': 9
}

quant_map = {
        'bb': 100,#100,#1000,
        'tp': 100,#100,#1000,
        'cnn': 50,#50,#500,
        'fox': 50,#50,#500,
        'nyt': 50,#25,#250,
        'wsj': 50,#25,#250,
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
        index.append(filename)
    return DataFrame(rows, index=index)

def read_files(path, classification):
    nfiles = quant_map[classification]
    listdir = os.listdir(path)
    random.shuffle(listdir)
    for article in listdir[:nfiles]:
        with open(os.path.join(path, article)) as f:
            text = f.read()
        yield os.path.join(path, article), text

tfidf = TfidfVectorizer()
data = build_corpus(SOURCES)
#tfidf.fit(data['text'])
#print(tfidf.vocabulary_)
#for k,v in sorted(vocab.items())[101:200]:
#    print(k, v)
X = tfidf.fit_transform(data['text'])#.toarray()
X = linear_kernel(X)

n_neighbors = 30
n_components = 3
fig = plt.figure(figsize=(15, 8))
plt.suptitle("Manifold Learning: {} neighbors".format(n_neighbors))

methods = ['standard', 'ltsa', 'modified']#, 'hessian']
labels = ['LLE', 'LTSA', 'Modified LLE', 'Hessian LLE']
for i, method in enumerate(methods):
    t0 = time()
    Y = manifold.LocallyLinearEmbedding(n_neighbors, n_components,
                                        eigen_solver='auto',
                                        method=method).fit_transform(X)
    t1 = time()
    print("%s: %.2g sec" % (methods[i], t1-t0))

    ax = fig.add_subplot(241 + i, projection='3d')
    ax.scatter(Y[:, 0], Y[:, 1], Y[:, 2], c=data['class'])
    plt.title("%s (%.2g sec)" % (labels[i], t1-t0))
    #ax.xaxis.set_major_formatter(NullFormatter())
    #ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')

# Isomap
t0 = time()
Y = manifold.Isomap(n_neighbors, n_components).fit_transform(X)
t1 = time()
print("isomap: %.2g sec" % (t1-t0))
ax = fig.add_subplot(245, projection='3d')
ax.scatter(Y[:, 0], Y[:, 1], Y[:, 2], c=data['class'])
plt.title("Isomap: %.2g sec" % (t1-t0))
#ax.xaxis.set_major_formatter(NullFormatter())
#ax.yaxis.set_major_formatter(NullFormatter())
plt.axis('tight')

# MDS
t0 = time()
mds = manifold.MDS(n_components, max_iter=100, n_init=1)
Y = mds.fit_transform(X)
t1 = time()
print("mds: %.2g sec" % (t1-t0))
ax = fig.add_subplot(246, projection='3d')
ax.scatter(Y[:, 0], Y[:, 1], Y[:, 2], c=data['class'])
plt.title("MDS: %.2g sec" % (t1-t0))
#ax.xaxis.set_major_formatter(NullFormatter())
#ax.yaxis.set_major_formatter(NullFormatter())
plt.axis('tight')

# Spectral Embedding
t0 = time()
se = manifold.SpectralEmbedding(n_components=n_components, n_neighbors=n_neighbors)
Y = se.fit_transform(X)
t1 = time()
print("spectralembedding: %.2g sec" % (t1-t0))
ax = fig.add_subplot(247, projection='3d')
ax.scatter(Y[:, 0], Y[:, 1], Y[:, 2], c=data['class'])
plt.title("SpectralEmbedding: %.2g sec" % (t1-t0))
#ax.xaxis.set_major_formatter(NullFormatter())
#ax.yaxis.set_major_formatter(NullFormatter())
plt.axis('tight')

# TSNE
t0 = time()
tsne = manifold.TSNE(n_components=n_components, init='pca', random_state=0)
Y = tsne.fit_transform(X)
t1 = time()
print("t-SNE: %.2g sec" % (t1-t0))
ax = fig.add_subplot(248, projection='3d')
ax.scatter(Y[:, 0], Y[:, 1], Y[:, 2], c=data['class'])
plt.title("t-SNE: %.2g sec" % (t1-t0))
#ax.xaxis.set_major_formatter(NullFormatter())
#ax.yaxis.set_major_formatter(NullFormatter())
plt.axis('tight')


plt.show()

#print(data.loc[data.index[0]]['class'])
