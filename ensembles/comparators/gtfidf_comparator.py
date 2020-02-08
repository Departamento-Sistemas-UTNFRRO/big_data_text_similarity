from gensim import corpora, models, similarities
from ensembles.comparators.comparator import Comparator
import numpy as np


class GTFIDFComparator(Comparator):
    STOPWORDS = []
    MODEL = None
    DICTIONARY = None
    NUMBER_OF_TOKENS = 0

    def __init__(self):
        self.STOPWORDS = super().get_stopwords()

    def train(self, questions_path):
        # get questions
        with open(questions_path, 'r') as ifile:
            questions = ifile.readlines()

        # remove stop words and tokenize
        texts = [[word for word in document.lower().split() if word not in self.STOPWORDS]
                 for document in questions]

        self.DICTIONARY = corpora.Dictionary(texts)
        self.NUMBER_OF_TOKENS = len(self.DICTIONARY)
        corpus = [self.DICTIONARY.doc2bow(text) for text in texts]

        self.MODEL = models.TfidfModel(corpus)

    def must_train(self):
        return True

    def compare(self, question1, question2):
        if not(question1 and question2):
            return 0.0

        if question1 == question2:
            return 1.0

        question1_vec = self.DICTIONARY.doc2bow(question1.lower().split())
        question2_vec = self.DICTIONARY.doc2bow(question2.lower().split())

        question1_rep = self.MODEL[question1_vec]
        question2_rep = self.MODEL[question2_vec]

        new_corpus = []
        new_corpus.append(question1_rep), new_corpus.append(question2_rep)
        index = similarities.MatrixSimilarity(new_corpus, num_features=self.NUMBER_OF_TOKENS)

        sims = index[new_corpus]

        return np.float64(sims[0][1]).item()
