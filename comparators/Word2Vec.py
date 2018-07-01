import os
import os.path
import pickle
import numpy as np
from comparators.Comparator import Comparator


class Word2Vec(Comparator):
    FILES_PATH = 'internal'
    MODEL_FILE = 'w2vDictionary'

    def __init__(self, vector_length=300):
        self.files_path = os.path.join('internal', 'word2vec')
        model_file_path = os.path.join(os.getcwd(), self.files_path, self.MODEL_FILE)
        self.model = self.load_obj(model_file_path)
        self.dim = vector_length

        if not os.path.exists(self.files_path):
            os.makedirs(self.files_path)

    def load_obj(self, name):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f, encoding='latin1')

    def must_train(self):
        return False

    def train(self, questions_path):
        return

    def compare(self, question1, question2):
        word_vector1 = self.prepare_vectors(question1)
        word_vector2 = self.prepare_vectors(question2)

        question_vector1 = super().calculate_question_vector_sum(word_vector1)
        question_vector2 = super().calculate_question_vector_sum(word_vector2)

        return super().calculate_distance(question_vector1, question_vector2)

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
