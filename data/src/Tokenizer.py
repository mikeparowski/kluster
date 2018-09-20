from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import json, os, codecs, sys, string, re


class Tokenizer():
    def __init__(self, source=None, directory=None):
        self.source = source
        self.directory = directory
        self.stopwords = stopwords.words('english')
        self.tokenizer = RegexpTokenizer("[\w']+", flags=re.UNICODE)
        self.translator = str.maketrans('', '', string.punctuation)

    def extract_clean(self):
        if not self.directory:
            print("ERROR: directory must be given for extract_clean. Use clean() for plaintext")
            sys.exit(1)
        print("extracting {}".format(self.source))
        filelist = os.listdir(self.directory)
        for filename in filelist:
            print(filelist.index(filename))
            with codecs.open(os.path.join(self.directory, filename), 'r', 'utf-8') as f:
                try:
                    data = f.read()
                    #data = json.load(f)
                except ValueError as e:
                    print("{} gave error: {}".format(filename, e))
                    sys.exit(1)
            article = data#['article']
            article = self.clean(article)
            with codecs.open('./'+self.source+'/'+filename, 'w', 'utf-8') as f:
                f.write(article)

    def clean(self, text):
        text = re.sub(r"[^\x00-\x7F]+", " ", text)
        # remove punctuation
        text = text.translate(self.translator)
        text = re.sub(r"US", "american", text)
        text = text.lower().split()
        tokens = [token for token in text if token not in self.stopwords and len(token) >= 3]
        text = " ".join(tokens)

        # regex cleaning
        text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
        text = re.sub(r"what's", "what is ", text)
        text = re.sub(r" s ", " ", text)
        text = re.sub(r"\'s", " ", text)
        text = re.sub(r"\'ve", " have ", text)
        text = re.sub(r"n't", " not ", text)
        text = re.sub(r"i'm", "i am ", text)
        text = re.sub(r"\'re", " are ", text)
        text = re.sub(r"\'d", " would ", text)
        text = re.sub(r"\'ll", " will ", text)
        text = re.sub(r"e ?- ?mail", "email", text)
        text = re.sub(r",", " ", text)
        text = re.sub(r"\.", " ", text)
        text = re.sub(r"!", " ! ", text)
        text = re.sub(r"\/", " ", text)
        text = re.sub(r"\^", " ^ ", text)
        text = re.sub(r"\+", " + ", text)
        text = re.sub(r"\-", " - ", text)
        text = re.sub(r"\=", " = ", text)
        text = re.sub(r"'", " ", text)
        text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
        text = re.sub(r":", " : ", text)
        text = re.sub(r" e g ", " eg ", text)
        text = re.sub(r" b g ", " bg ", text)
        text = re.sub(r" u s ", " american ", text)
        text = re.sub(r"\0s", "0", text)
        text = re.sub(r" 9 11 ", "911", text)
        text = re.sub(r"j k", "jk", text)
        text = re.sub(r"\s{2,}", " ", text)

        # stemming
        #text = text.split()
        #stemmer = SnowballStemmer('english')
        #stemmed_words = [stemmer.stem(word) for word in text]
        #text = " ".join(stemmed_words)
        tokens = self.tokenizer.tokenize(text)
        return " ".join(tokens)

if __name__ == "__main__":
    extract('./breitbart-json/articles/', 'breitbart')
    extract('./thinkprogress-json/articles/', 'thinkprogress')

