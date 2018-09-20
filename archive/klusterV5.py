import os, random, numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.manifold import LocallyLinearEmbedding
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import KFold
from xgboost import XGBClassifier
from pandas import DataFrame
import pickle

REP = "republican"
DEM = "democrat"

SOURCES = [
    ('data/breitbart', REP),
    ('data/thinkprogress', DEM),
    ('data/cnn', DEM),
    ('data/foxnews', REP),
    ('data/nytimes', DEM),
    ('data/theatlantic', DEM),
    ('data/theblaze', REP),
    ('data/thefederalist', REP),
    ('data/vice', DEM),
    ('data/wsj', REP)
]

class Classifier:

    def __init__(self, vectorizer, clf, labels=None, ncomponents=500, nsplits=6):
        self.vectorizer = vectorizer
        self.clf = clf
        self.labels = labels
        self.ncomponents = ncomponents
        self.nsplits = nsplits
        self.svd = ('svd', TruncatedSVD(algorithm='randomized', n_components=self.ncomponents))
        self.data = DataFrame({'text': [], 'class': []})
        self.pipeline = Pipeline([
            self.vectorizer,
            self.svd,
            self.clf
        ])

        self.scores = []
        self.confusion = np.array([[0, 0], [0, 0]])

    def train(self):
        train_text = self.data['text'].values
        train_y = self.data['class'].values
        self.pipeline.fit(train_text, train_y)

    def predict(self, text):
        return self.pipeline.predict_proba([text])

    def train_test(self):
        k_fold = KFold(n_splits=self.nsplits)
        for train_indices, test_indices in k_fold.split(self.data):
            train_text = self.data.iloc[train_indices]['text'].values
            print type(train_text)
            train_y = self.data.iloc[train_indices]['class'].values

            test_text = self.data.iloc[test_indices]['text'].values
            test_y = self.data.iloc[test_indices]['class'].values

            self.pipeline.fit(train_text, train_y)
            predictions = self.pipeline.predict(test_text)

            self.confusion += confusion_matrix(test_y, predictions)
            self.scores.append(f1_score(test_y, predictions, labels=self.labels, average=None))
        
    def build_corpus(self, sources):
        for path, classification in sources:
            self.data = self.data.append(self._build_data_frame(path, classification))
        self.data = self.data.reindex(np.random.permutation(self.data.index))

    def _read_files(self, path):
        for article in os.listdir(path):
            with open(os.path.join(path, article)) as f:
                text = f.read()
            yield os.path.join(path, article), text

    def _build_data_frame(self, path, classification):
        rows = []
        index = []
        for filename, text in self._read_files(path):
            rows.append({'text': text, 'class': classification})
            index.append(filename)
        return DataFrame(rows, index=index)

    def save(self, model):
        f = open(model, 'wb+')
        pickle.dump(self.pipeline, f)
        f.close()

    def load(self, model):
        f = open(model, 'rb')
        self.pipeline = pickle.load(f)
        f.close()

    def get_scores(self):
        return self.scores
    
    def get_confusion(self):
        return self.confusion

def run(classifier, loaded_model=None):
    clf = Classifier(('tfidf', TfidfVectorizer()), ('clf', classifier), [REP, DEM])
    if loaded_model:
        clf.load(loaded_model)
        #with open('./data/huffingtonpost/huffpost.txt') as f:
        #    article = f.read()
        #pred = clf.predict(whatever)
        return pred if pred else 0

    clf.build_corpus(SOURCES)
    clf.train()

def score(clf):
    print "Total articles classified: {}".format(len(clf.data))
    print "Score: {}".format(sum(clf.scores)/len(clf.scores))
    print "Confusion Matrix:"
    print "{}".format(clf.confusion)

if __name__ == '__main__':
    run(XGBClassifier())
    #run(KMeans()) <-- figure this out next

