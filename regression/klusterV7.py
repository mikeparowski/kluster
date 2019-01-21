import os, sys, random, numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.base import BaseEstimator, TransformerMixin
import matplotlib.pyplot as plt
from pandas import DataFrame
from utils import build_corpus

class PrepareText(BaseEstimator, TransformerMixin):
    def __init__(self, vectorizer='count', svd=False, ngram_range=(1,1), max_df=1.0, min_df=1, norm='l2', n_components=2):
        self.vectorizer = vectorizer
        self.svd = svd
        self.ngram_range = ngram_range
        self.max_df = max_df
        self.min_df = min_df
        self.norm = norm
        self.n_components = n_components
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        if self.vectorizer == 'tfidf':
            vec = TfidfVectorizer(ngram_range=self.ngram_range, max_df=self.max_df, min_df=self.min_df, self.norm=norm)
        else:
            vec = CountVectorizer(ngram_range=self.ngram_range, max_df=self.max_df, min_df=self.min_df)
        X = vec.fit_transform(X)
        if self.svd:



