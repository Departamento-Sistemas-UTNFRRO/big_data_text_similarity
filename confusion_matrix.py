import csv
import os.path
from argparse import ArgumentParser
from datetime import datetime

import numpy as np
import utils.general_utils as gu

from utils import common_utils as cu
from utils import io_utils

logger = gu.get_logger(__name__)


def create_confusion_matrix(real_relations, pair_distances, threshold):
    confusion_matrix = [[0, 0], [0, 0]]

    guessed_relations = np.array([1 if pair_distances[i] <= threshold else 0 for i in range(len(real_relations))])

    confusion_matrix[0][0] = ((real_relations == 0) * (guessed_relations == 0)).mean()
    confusion_matrix[0][1] = ((real_relations == 0) * (guessed_relations == 1)).mean()
    confusion_matrix[1][0] = ((real_relations == 1) * (guessed_relations == 0)).mean()
    confusion_matrix[1][1] = ((real_relations == 1) * (guessed_relations == 1)).mean()

    return confusion_matrix


def start(technique, runs, distances_path, sample_size, sample_path):
    logger.info('Starting script confusion_matrix.')
    start_time = datetime.now()

    io_utils.create_directory('results')

    # Contains the best threshold and its error for each sample
    threshold_errors = []
    confusion_matrix = []

    avg_threshold = 0

    # This will generate a confusion matrix per sample.
    for run in range(1, runs + 1):
        sample_questions = io_utils.read_sample_file(sample_path, sample_size, run)
        distances = io_utils.read_distances_file(distances_path, technique, run)

        real_relations = np.zeros(sample_size)
        pair_distances = []
        for i in range(sample_size):
            real_relations[i] = int(sample_questions[i][4])
            pair_distances.append(float(distances[i][1]))

        threshold = cu.find_best_threshold(real_relations, pair_distances, sample_size)
        error = cu.compute_validation_error(real_relations, pair_distances, threshold, sample_size)

        threshold_errors.append([threshold, error])

        if run < runs:
            avg_threshold += threshold
        else:
            # Computes the confusion matrix with the last sample
            avg_threshold = avg_threshold / (runs - 1)

            logger.info('Threshold used in confusion matrix: ' + str(avg_threshold))

            confusion_matrix = create_confusion_matrix(real_relations, pair_distances, avg_threshold)

    # Writes threshold and errors in a file
    error_results_path = os.path.join('results', 'errors_'
                                      + technique + '_' + '{:%Y%m%d_%H%M%S}'.format(datetime.now()) + '.csv')
    with open(error_results_path, 'w') as errors_file:
        writer = csv.writer(errors_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(threshold_errors)

    # Writes confusion matrix in a file
    matrix_results_path = os.path.join('results', 'confusionMatrix_'
                                       + technique + '_' + '{:%Y%m%d_%H%M%S}'.format(datetime.now()) + '.csv')
    with open(matrix_results_path, 'w') as matrix_file:
        writer = csv.writer(matrix_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(confusion_matrix)

    logger.info('Script finished. Total time: ' + str(datetime.now() - start_time))

    print('Confusion Matrix:')
    print('=================')
    print('\t' + "%.4f" % confusion_matrix[0][0] + '\t' + "%.4f" % confusion_matrix[0][1])
    print('\t' + "%.4f" % confusion_matrix[1][0] + '\t' + "%.4f" % confusion_matrix[1][1])


if __name__ == '__main__':
    parser = ArgumentParser('Computes the confusion matrix of a comparison technique')

    parser.add_argument('-technique', dest='technique', required=True,
                        choices=['bow', 'tfidf', 'gtfidf', 'w2v', 'ft', 'sem', 'ens'])
    parser.add_argument('-runs', dest='runs', default=1, type=int, help='Total runs number')
    parser.add_argument('-n', dest='sample_size', default=0, type=int,
                        help='Questions subset size that will be processed (0 -> all the questions)')
    parser.add_argument('-input_path', dest='input_path', default='/tmp',
                        help='Path where the samples and distances files will be saved')
    parser.add_argument('-samples-path', dest='sample_path', default='/tmp/samples',
                        help='Path to sample file (if not provided, creates a new sample)')

    args = parser.parse_args()

    start(args.technique,
          args.runs,
          args.input_path,
          args.sample_size,
          args.sample_path)
