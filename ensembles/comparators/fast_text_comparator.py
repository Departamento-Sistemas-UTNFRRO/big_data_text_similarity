import os, os.path, fasttext
import numpy as np

from ensembles.comparators.comparator import Comparator


class FTComparator(Comparator):
    def __init__(self):
        self.files_path = os.path.join('internal', 'fasttext')
        self.model = None
        self.dim = 100

        if not os.path.exists(self.files_path):
            os.makedirs(self.files_path)

    def must_train(self):
        return True

    def train(self, questions_path, vector_length=100):
        self.dim = vector_length
        self.model = fasttext.train_unsupervised(questions_path, model='skipgram', dim=self.dim, thread=8)

    def compare(self, question1, question2):
        if not(question1 and question2):
            return 0.0

        if question1 == question2:
            return 1.0

        sentence_vector1 = self.prepare_vectors(question1)
        sentence_vector2 = self.prepare_vectors(question2)

        question_vector1 = super().calculate_question_vector_avg(sentence_vector1)
        question_vector2 = super().calculate_question_vector_avg(sentence_vector2)

        return super().calculate_similarity(question_vector1, question_vector2)

    def prepare_vectors(self, question):
        words = question.split()

        if len(words) != 0:
            vectors = np.zeros([len(words), self.dim])

            for i, word in enumerate(words):
                if word in self.model:
                    vectors[i] = np.array(self.model[word])

            return vectors
        else:
            return np.zeros(self.dim)
