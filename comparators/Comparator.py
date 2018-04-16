import numpy as np


class Comparator(object):
    def get_stopwords(self):
        stopwords = []
        with open('data/stopwords.txt', 'r') as input_file:
            for line in input_file:
                line = ''.join(line.split())
                stopwords.append(line)
        return stopwords

    def compare(self, question1, question2):
        """ Returns the distance between 2 questions
        """
        raise NotImplementedError('Override method!')

    def must_train(self):
        raise NotImplementedError('Override method!')

    def train(self, questions_path):
        pass

    def calculate_question_vector_sum(self, vectors):
        return vectors.sum(axis=0)

    def calculate_question_vector_avg(self, vectors):
        return vectors.mean(axis=0)

    def calculate_distance(self, vector1, vector2):
        if np.any(vector1) and np.any(vector2):
            n1 = np.linalg.norm(vector1)
            n2 = np.linalg.norm(vector2)
            similarity = np.dot(vector1, vector2) / n1 / n2
        else:
            # If at least one of the vectors contains all zeros, similarity cannot be concluded
            similarity = 0

        return 1 - similarity
