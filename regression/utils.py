import pandas as pd
import numpy as np
import random, os

SOURCES = [
    ('data/articles/breitbart', 'bb'),
    ('data/articles/thinkprogress', 'tp')
]

ext_map = {
    'bb': 0,
    'tp': 1
}

quant_map = {
    'bb': 5000,
    'tp': 5000
}

def build_corpus(sources):
    data = pd.DataFrame({'text': [], 'title': [], 'class': []})
    for path, classification in sources:
        data = data.append(build_data_frame(path, classification))
    return data.reindex(np.random.permutation(data.index))

def build_data_frame(path, classification):
    rows = []
    for filename, text in read_files(path, classification):
        rows.append({'text': text, 'title': filename[:-3], 'class': ext_map[classification]})
    return pd.DataFrame(rows)

def read_files(path, classification):
    nfiles = quant_map[classification]
    listdir = os.listdir(path)
    random.shuffle(listdir)
    for article in listdir[:nfiles]:
        with open(os.path.join(path, article)) as f:
            text = f.read()
        yield article, text
