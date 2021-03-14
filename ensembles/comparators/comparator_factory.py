import os
from utils import general_utils as gu
from ensembles.comparators.bow_comparator import BowComparator
from ensembles.comparators.fast_text_comparator import FTComparator
from ensembles.comparators.w2v_comparator import W2VComparator
from ensembles.comparators.tfidf_comparator import TFIDFComparator
from ensembles.comparators.gtfidf_comparator import GTFIDFComparator
from ensembles.comparators.semantic_comparator import SemComparator


class ComparatorFactory(object):
    def __init__(self):
        self.QUESTION1_COL = 1
        self.QUESTION2_COL = 2

        self.comparator = None

    def __create_comparator(self, technique):
        if technique.startswith('bow'):
            self.comparator = BowComparator()
        elif technique.startswith('tfidf'):
            self.comparator = TFIDFComparator()
        elif technique.startswith('gtfidf'):
            self.comparator = GTFIDFComparator()
        elif technique.startswith('w2v'):
            self.comparator = W2VComparator()
        elif technique.startswith('ft'):
            self.comparator = FTComparator()
        elif technique.startswith('sem'):
            self.comparator = SemComparator()

    def get_comparator(self, technique, questions=None, re_generate_corpus=False):
        if self.comparator is None:
            self.__create_comparator(technique)

        if self.comparator.must_train():
            gu.print_screen('Training model...')

            questions_run_dir = os.path.join('internal', 'questions')
            questions_run_file = os.path.join(questions_run_dir, 'questions.txt')

            if not os.path.exists(questions_run_dir):
                os.makedirs(questions_run_dir)

            if re_generate_corpus:
                self.create_questions_file(questions_run_file, questions)
            self.comparator.train(questions_run_file)

        return self.comparator

    @staticmethod
    def create_questions_file(file_name, data_questions):
        # Creates a file with the questions
        with open(file_name, 'w') as questions:
            for question in data_questions:
                questions.write(question + '\n')
