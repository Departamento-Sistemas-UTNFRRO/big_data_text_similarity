import csv
import os.path
from argparse import ArgumentParser
from datetime import datetime

import numpy as np

from utils import common_utils as cu
from utils import general_utils as gu
from utils import io_utils

QUESTION1_COL = 1
QUESTION2_COL = 2


def create_confusion_matrix(real_relations, pair_distances, threshold):
    confusion_matrix = [[0, 0], [0, 0]]

    guessed_relations = np.array([1 if pair_distances[i] <= threshold else 0 for i in range(len(real_relations))])

    confusion_matrix[0][0] = ((real_relations == 0) * (guessed_relations == 0)).mean()
    confusion_matrix[0][1] = ((real_relations == 0) * (guessed_relations == 1)).mean()
    confusion_matrix[1][0] = ((real_relations == 1) * (guessed_relations == 0)).mean()
    confusion_matrix[1][1] = ((real_relations == 1) * (guessed_relations == 1)).mean()

    return confusion_matrix


def write_confusion_matrix(matrix_results_path, confusion_matrix):
    with open(matrix_results_path, 'a') as matrix_file:
        writer = csv.writer(matrix_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        row = [[0, 0, 0, 0]]
        row[0][0] = confusion_matrix[0][0]
        row[0][1] = confusion_matrix[0][1]
        row[0][2] = confusion_matrix[1][0]
        row[0][3] = confusion_matrix[1][1]
        writer.writerows(row)


def write_error_report(path, threshold_errors, technique, sample_size):
    with open(path, 'a') as errors_file:
        writer = csv.writer(errors_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)

        sum_error = 0
        for threshold_row in threshold_errors:
            row = [["", 0, 0]]
            row[0][0] = technique
            row[0][1] = sample_size
            row[0][2] = threshold_row[1]
            sum_error += threshold_row[1]
            writer.writerows(row)

        row = [["", 0, 0.0]]
        row[0][0] = technique
        row[0][1] = sample_size
        row[0][2] = (sum_error / len(threshold_errors))
        writer.writerows(row)


if __name__ == '__main__':
    start_time = datetime.now()

    gu.print_screen('Starting script.')

    parser = ArgumentParser('Computes the confusion matrix of a comparison technique')

    parser.add_argument('-technique', dest='technique', required=True,
                        choices=['bow', 'tfidf', 'gtfidf', 'w2v', 'ft', 'sem', 'ens'])
    parser.add_argument('-runs', dest='runs', default=1, type=int, help='Total runs number')
    parser.add_argument('-n', dest='sample_size', default=0, type=int,
                        help='Questions subset size that will be processed (0 -> all the questions)')
    parser.add_argument('-samples_path', dest='samples_path', default='/tmp',
                        help='Path where the samples files will be saved')
    parser.add_argument('-input_path', dest='input_path', default='/tmp',
                        help='Path where the distances files will be saved')

    args = parser.parse_args()
    technique = args.technique
    runs = args.runs
    samples_path = args.samples_path
    input_path = args.input_path
    sample_size = args.sample_size

    io_utils.create_directory('results')

    threshold_errors = []  # Contains the best threshold and its error for each sample
    confusion_matrix = []

    avg_threshold = 0

    error_results_path = os.path.join('results', 'errors_' + technique + '_' + '{:%Y%m%d_%H%M%S}'.format(datetime.now()) + '.csv')
    error_report = os.path.join('results', 'z_errors_report_' + technique + '_' + str(sample_size) + '.csv')
    matrix_results_path = os.path.join('results', 'confusionMatrix_' + technique + '_' + str(sample_size) + '_' + '{:%Y%m%d_%H%M%S}'.format(datetime.now()) + '.csv')

    total_confusion_matrix = [[0, 0], [0, 0]]
    for run in range(1, runs + 1):
        sample_questions = io_utils.read_sample_file(samples_path, sample_size, run)
        distances = io_utils.read_distances_file(input_path, technique, run)
        sample_size = sample_size if sample_size != 0 else len(sample_questions)

        real_relations = np.zeros(sample_size)
        pair_distances = []

        for i in range(sample_size):
            real_relations[i] = int(sample_questions[i][4])
            pair_distances.append(float(distances[i][1]))

        threshold = cu.find_best_threshold(real_relations, pair_distances, sample_size)
        error = cu.compute_validation_error(real_relations, pair_distances, threshold, sample_size)

        threshold_errors.append([threshold, error])

        if run < runs:
            confusion_matrix = create_confusion_matrix(real_relations, pair_distances, threshold)
            write_confusion_matrix(matrix_results_path, confusion_matrix)

            avg_threshold += threshold
        else:
            # Computes the confusion matrix with the last sample
            if runs > 1:
                avg_threshold = avg_threshold / (runs - 1)
            else:
                avg_threshold = threshold

            gu.print_screen('Threshold used in confusion matrix: ' + str(avg_threshold))

            confusion_matrix = create_confusion_matrix(real_relations, pair_distances, threshold)
            write_confusion_matrix(matrix_results_path, confusion_matrix)

        total_confusion_matrix[0][0] += confusion_matrix[0][0]
        total_confusion_matrix[0][1] += confusion_matrix[0][1]
        total_confusion_matrix[1][0] += confusion_matrix[1][0]
        total_confusion_matrix[1][1] += confusion_matrix[1][1]

    with open(error_results_path, 'w') as errors_file:
        writer = csv.writer(errors_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(threshold_errors)

    write_error_report(error_report, threshold_errors, technique, sample_size)

    total_confusion_matrix[0][0] = total_confusion_matrix[0][0] / runs
    total_confusion_matrix[0][1] = total_confusion_matrix[0][1] / runs
    total_confusion_matrix[1][0] = total_confusion_matrix[1][0] / runs
    total_confusion_matrix[1][1] = total_confusion_matrix[1][1] / runs
    write_confusion_matrix(matrix_results_path, total_confusion_matrix)

    gu.print_screen('Script finished. Total time: ' + str(datetime.now() - start_time))

    print('Confusion Matrix. Technique {0}, Sample Size {1}'.format(technique, str(sample_size)))
    print('=================')
    print('\t' + "%.4f" % total_confusion_matrix[0][0] + '\t' + "%.4f" % total_confusion_matrix[0][1])
    print('\t' + "%.4f" % total_confusion_matrix[1][0] + '\t' + "%.4f" % total_confusion_matrix[1][1])
    print('=================\n\n')
