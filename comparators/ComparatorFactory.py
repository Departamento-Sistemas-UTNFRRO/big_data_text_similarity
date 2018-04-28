import os
from utils import general_utils as gu
from comparators.BagOfWordsComparator import BagOfWordsComparator
from comparators.FastTextComparator import FastTextComparator
from comparators.Word2VecComparator import Word2VecComparator
from comparators.TFIDFComparator import TFIDFComparator
from comparators.GensimTFIDFComparator import GensimTFIDFComparator
from comparators.SemanticComparator import SemanticComparator


class ComparatorFactory(object):
    def __init__(self):
        self.QUESTION1_COL = 1
        self.QUESTION2_COL = 2

        self.comparator = None

    def create_comparator(self, technique):
        if technique == 'bow':
            self.comparator = BagOfWordsComparator()
        elif technique == 'tfidf':
            self.comparator = TFIDFComparator()
        elif technique == 'gtfidf':
            self.comparator = GensimTFIDFComparator()
        elif technique == 'w2v':
            self.comparator = Word2VecComparator()
        elif technique == 'ft':
            self.comparator = FastTextComparator()
        elif technique == 'sem':
            self.comparator = SemanticComparator()

    def get_comparator(self, technique, questions):
        if self.comparator is None:
            self.create_comparator(technique)

        if self.comparator.must_train():
            gu.print_screen('Training model...')

            questions_run_dir = os.path.join('internal', 'questions')
            questions_run_file = os.path.join(questions_run_dir, 'questions.txt')

            if not os.path.exists(questions_run_dir):
                os.makedirs(questions_run_dir)

            self.create_questions_file(questions_run_file, questions)

            self.comparator.train(questions_run_file)

        return self.comparator

    def create_questions_file(self, file_name, data_questions):
        # Creates a file with the questions
        with open(file_name, 'w') as questions:
            for question in data_questions:
                questions.write(question + '\n')
