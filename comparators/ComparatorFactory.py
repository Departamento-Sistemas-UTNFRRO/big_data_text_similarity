import os
import logging
from comparators.BagOfWords import BagOfWords
from comparators.FastText import FastText
from comparators.Word2Vec import Word2Vec
from comparators.TFIDF import TFIDF
from comparators.GensimTFIDF import GensimTFIDF
from comparators.Semantic import Semantic


class ComparatorFactory(object):
    def __init__(self):
        self.QUESTION1_COL = 1
        self.QUESTION2_COL = 2

        self.comparator = None

    def create_comparator(self, technique):
        if technique == 'bow':
            self.comparator = BagOfWords()
        elif technique == 'tfidf':
            self.comparator = TFIDF()
        elif technique == 'gtfidf':
            self.comparator = GensimTFIDF()
        elif technique == 'w2v':
            self.comparator = Word2Vec()
        elif technique == 'ft':
            self.comparator = FastText()
        elif technique == 'sem':
            self.comparator = Semantic()

    def get_comparator(self, technique, questions):
        if self.comparator is None:
            self.create_comparator(technique)

        if self.comparator.must_train():
            logging.info('Training model...')

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
