from ensembles.comparators.comparator import Comparator
from sklearn.feature_extraction.text import TfidfVectorizer


class TFIDFComparator(Comparator):
    def __init__(self):
        stopwords = super().get_stopwords()
        # Initialize model
        self.model = TfidfVectorizer(stop_words=stopwords)

    def train(self, questions_path):
        # Open questions_path file and get a list from all the questions in it
        with open(questions_path, 'r') as ifile:
            questions = ifile.readlines()

        # Train model with pair of questions
        self.model.fit_transform(questions)

    def must_train(self):
        return True

    def compare(self, question1, question2):
        """ Calculate distance between question1 and question2
        """
        if not(question1 and question2):
            return 0.0

        if question1 == question2:
            return 1.0

        # set list of size 2 to send to model
        questions = [question1, question2]

        # get tfidf representation of the given pair of questions
        question_rep = self.model.transform(questions)
        question_rep = question_rep.toarray()

        # get distance from father's method
        return super().calculate_similarity(question_rep[0], question_rep[1])
