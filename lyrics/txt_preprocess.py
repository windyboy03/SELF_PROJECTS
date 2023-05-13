import nltk
from nltk.corpus import stopwords
import os

stop_words = stopwords.words('english')
prt = nltk.stem.PorterStemmer()

def preprocess(document_path):

    with open(document_path, 'r') as file:
        document = file.read()

    tokens = nltk.word_tokenize(document)

    tokens_pun_lower = [i.lower() for i in tokens if i.isalnum()]

    tokens_stop = [i for i in tokens_pun_lower if i not in stop_words]

    terms = [prt.stem(i) for i in tokens_stop]

    return " ".join(terms)

#%%
