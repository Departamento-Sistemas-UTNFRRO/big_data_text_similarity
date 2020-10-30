from math import sqrt
import numpy as np

from ensembles.comparators.comparator import Comparator


class BowComparator(Comparator):

    def must_train(self):
        return False

    def __init__(self):
        self.stopwords = super().get_stopwords()

    def create_words_vector(self, vector1, vector2):
        stopwords_set = set(self.stopwords)
        wv1 = set(vector1).difference(stopwords_set)
        wv2 = set(vector2).difference(stopwords_set)

        return wv1.union(wv2)

    @staticmethod
    def count_repetitions(words, vector):
        repetitions = np.zeros(len(words))

        for i, word in enumerate(words):
            for v1 in vector:
                if v1 == word:
                    repetitions[i] += 1

        return repetitions

    def compare(self, question_1, question_2):
        similarity = 0.0

        if question_1 == question_2:
            return 1.0

        if not(question_1 and question_2):
            return 0.0

        vector1 = question_1.split()
        vector2 = question_2.split()

        words = self.create_words_vector(vector1, vector2)

        if len(words) > 0:
            u = self.count_repetitions(words, vector1)
            v = self.count_repetitions(words, vector2)

            if np.any(u) and np.any(v):
                # similarity = 1 - cosine_distance
                similarity = np.dot(u, v) / (sqrt(np.dot(u, u)) * sqrt(np.dot(v, v)))
                similarity = np.float64(similarity).item()

        return similarity
