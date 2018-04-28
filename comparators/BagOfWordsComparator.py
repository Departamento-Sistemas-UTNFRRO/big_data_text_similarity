import numpy as np
from nltk import cluster
from comparators.Comparator import Comparator


class BagOfWordsComparator(Comparator):
    def __init__(self):
        self.stopwords = super().get_stopwords()

    def must_train(self):
        return False

    def compare(self, question1, question2):
        vector1 = question1.split()
        vector2 = question2.split()

        words = self.create_words_vector(vector1, vector2)

        if len(words) > 0:
            repetitions1 = self.count_repetitions(words, vector1)
            repetitions2 = self.count_repetitions(words, vector2)

            if np.any(repetitions1) and np.any(repetitions2):
                return cluster.util.cosine_distance(repetitions1, repetitions2)

        # If it gets here, distance could not be concluded
        return 1

    def create_words_vector(self, vector1, vector2):
        words = []

        for v1 in vector1:
            if v1 not in words and v1 not in self.stopwords:
                words.append(v1)

        for v2 in vector2:
            if v2 not in words and v2 not in self.stopwords:
                words.append(v2)

        return words

    def count_repetitions(self, words, vector):
        repetitions = np.zeros(len(words))

        for i, word in enumerate(words):
            for v1 in vector:
                if v1 == word:
                    repetitions[i] += 1

        return repetitions
