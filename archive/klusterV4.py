import os, random, numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import KFold
from xgboost import XGBClassifier
from pandas import DataFrame

REP = "republican"
DEM = "democrat"

SOURCES = [
    ('data/breitbart', REP),
    ('data/thinkprogress', DEM)
]

def read_files(path):
    for article in os.listdir(path):
        with open(os.path.join(path, article)) as f:
            text = f.read()
        yield os.path.join(path, article), text

def build_data_frame(path, classification):
    rows = []
    index = []
    for filename, text in read_files(path):
        rows.append({'text': text, 'class': classification})
        index.append(filename)

    data_frame = DataFrame(rows, index=index)
    return data_frame

data = DataFrame({'text': [], 'class': []})
for path, classification in SOURCES:
    data = data.append(build_data_frame(path, classification))

data = data.reindex(np.random.permutation(data.index))
## now split files into training data and labels. probably tuple (filename, r/d)

classifier = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('svd', TruncatedSVD(algorithm='randomized', n_components=300)),
    ('clf', XGBClassifier())
])

#classifier.fit(data['text'].values, data['class'].values)

k_fold = KFold(n_splits=8)
scores = []
confusion = np.array([[0, 0], [0, 0]])
for train_indices, test_indices in k_fold.split(data):
    train_text = data.iloc[train_indices]['text'].values
    train_y = data.iloc[train_indices]['class'].values

    test_text = data.iloc[test_indices]['text'].values
    test_y = data.iloc[test_indices]['class'].values

    classifier.fit(train_text, train_y)
    predictions = classifier.predict(test_text)

    confusion += confusion_matrix(test_y, predictions)
    score = f1_score(test_y, predictions, labels=[REP, DEM], average=None)
    scores.append(score)

string =  "Total articles classified: {}\n".format(len(data))
string += "n_components = 500, kfolds=8\n"
string += "Score: {}\n".format(sum(scores)/len(scores))
string +=  "Confusion matrix:\n {}".format(confusion)
print string
with open('./results/results.txt', 'a+') as f:
    f.write(string)

