import os.path
import csv
import logging
from argparse import ArgumentParser
from datetime import datetime
from multiprocessing import Array
from utils import common_utils as cu
from utils import general_utils as gu
from comparators.ComparatorFactory import ComparatorFactory

QUESTION1_COL = 1
QUESTION2_COL = 2


def start_computation(technique, training_path, questions_path, num_training, num_workers, previous_path):
    start_time = datetime.now()

    if previous_path is None:
        if not os.path.exists('results'):
            os.mkdir('results')

        results_path = os.path.join('results', 'computeError_'
                                    + technique + '_' + '{:%Y%m%d_%H%M%S}'.format(datetime.now()) + '.csv')
    else:
        results_path = previous_path

        logging.info('Loading files...')

    data_training = []
    with open(training_path, 'r') as training_file:
        reader = csv.reader(training_file)
        next(reader)  # Ignores the first line

        for row in reader:
            data_training.append(row[1:])  # Ignores the first column

    data_questions = []
    with open(questions_path, 'r') as questions_file:
        reader = csv.reader(questions_file)
        next(reader)  # Ignores the first line

        for row in reader:
            data_questions.append(row)

    total_runs = len(data_training[0])
    run_number = gu.define_first_row(previous_path)

    factory = ComparatorFactory()

    with open(results_path, 'a') as results_file:
        writer = csv.writer(results_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if previous_path is None:
            writer.writerow(['Threshold', 'Error'])  # Header

        for run in range(run_number, total_runs):
            logging.info('Starting run ' + str(run + 1))

            # Prepares the IDs of this run and the training questions
            pair_ids = []
            training_questions = []
            for i, row in enumerate(data_training):
                pair_ids.append(int(row[run]))

                if i < num_training:
                    training_questions.append(data_questions[i][QUESTION1_COL])
                    training_questions.append(data_questions[i][QUESTION2_COL])

            comparator = factory.get_comparator(technique, training_questions)

            question_pairs, relations = cu.prepare_relations(pair_ids, data_questions)

            distances = Array('f', len(pair_ids))  # A shared array with all the distances
            cu.distribute_comparing_work(question_pairs, distances, num_workers, comparator)

            threshold = cu.find_best_threshold(relations, distances, num_training)

            error = cu.compute_validation_error(relations, distances, threshold, len(pair_ids))

            writer.writerow([threshold, error])

            logging.info('Run ' + str(run + 1) + ' finished.')

    logging.info('Script finished. Total time: ' + str(datetime.now() - start_time))


if __name__ == '__main__':
    gu.get_logger()
    logging.info('Starting script.')

    parser = ArgumentParser('Computes the average error of a comparison technique')

    parser.add_argument('-t', dest='technique', required=True, choices=['bow', 'tfidf', 'gtfidf', 'w2v', 'ft', 'sem'])
    parser.add_argument('-training', dest='training_path', required=True)
    parser.add_argument('-questions', dest='questions_path', required=True)
    parser.add_argument('-np', dest='number_training', required=True, type=int)

    parser.add_argument('-workers', dest='number_workers', default=5, type=int)
    parser.add_argument('-previous', dest='previous_path')

    args = parser.parse_args()

    start_computation(args.technique,
                      args.training_path,
                      args.questions_path,
                      args.number_training,
                      args.number_workers,
                      args.previous_path)
