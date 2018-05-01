import os.path
import csv
import numpy as np
from argparse import ArgumentParser
from datetime import datetime
from multiprocessing import Array
from utils import common_utils as cu
from utils import general_utils as gu
from comparators.ComparatorFactory import ComparatorFactory

QUESTION1_COL = 1
QUESTION2_COL = 2


def create_confusion_matrix(relations, distances, threshold, num_training):
    confusion_matrix = [[0, 0], [0, 0]]

    guessed_relations = \
        np.array([1 if distances[i] <= threshold else 0 for i in range(num_training, len(relations))])
    real_relations = relations[num_training:len(relations)]

    confusion_matrix[0][0] = ((real_relations == 0) * (guessed_relations == 0)).mean()
    confusion_matrix[0][1] = ((real_relations == 0) * (guessed_relations == 1)).mean()
    confusion_matrix[1][0] = ((real_relations == 1) * (guessed_relations == 0)).mean()
    confusion_matrix[1][1] = ((real_relations == 1) * (guessed_relations == 1)).mean()

    return confusion_matrix


if __name__ == '__main__':
    start_time = datetime.now()

    gu.print_screen('Starting script.')

    parser = ArgumentParser('Computes the confusion matrix of a comparison technique')

    parser.add_argument('-technique', dest='technique', required=True, choices=['bow', 'tfidf', 'gtfidf', 'w2v', 'ft', 'sem'])
    parser.add_argument('-training', dest='training_path', required=True)
    parser.add_argument('-questions', dest='questions_path', required=True)
    parser.add_argument('-threshold', dest='threshold', required=True, type=float)
    parser.add_argument('-np', dest='number_training', required=True, type=int)

    parser.add_argument('-workers', dest='number_workers', default=5, type=int)

    args = parser.parse_args()
    technique = args.technique
    training_path = args.training_path
    questions_path = args.questions_path
    avg_threshold = args.threshold
    num_training = args.number_training
    num_workers = args.number_workers

    if not os.path.exists('results'):
        os.mkdir('results')

    results_path = os.path.join('results', 'confusionMatrix_'
                                + technique + '_' + '{:%Y%m%d_%H%M%S}'.format(datetime.now()) + '.csv')

    gu.print_screen('Loading files...')

    data_training = []
    with open(training_path, 'r') as training_file:
        reader = csv.reader(training_file)

        for row in reader:
            data_training.append(row[1])  # Ignores the first column

    data_questions = []
    with open(questions_path, 'r') as questions_file:
        reader = csv.reader(questions_file)
        next(reader)  # Ignores the first line

        for row in reader:
            data_questions.append(row)

    pair_ids = []
    training_questions = []
    for i, pair_id in enumerate(data_training):
        pair_ids.append(int(pair_id))

        if i < num_training:
            training_questions.append(data_questions[i][QUESTION1_COL])
            training_questions.append(data_questions[i][QUESTION2_COL])

    comparator = ComparatorFactory().get_comparator(technique, training_questions)

    question_pairs, relations = cu.prepare_relations(pair_ids, data_questions)

    distances = Array('f', len(pair_ids))  # A shared array with all the distances
    cu.distribute_comparing_work(question_pairs, distances, num_workers, comparator)

    gu.print_screen('Computing confusion matrix')
    confusion_matrix = create_confusion_matrix(relations, distances, avg_threshold, num_training)

    with open(results_path, 'w') as results_file:
        writer = csv.writer(results_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(confusion_matrix)

    gu.print_screen('Script finished. Total time: ' + str(datetime.now() - start_time))

    print('Confusion Matrix:')
    print('=================')
    print('\t' + "%.4f" % confusion_matrix[0][0] + '\t' + "%.4f" % confusion_matrix[0][1])
    print('\t' + "%.4f" % confusion_matrix[1][0] + '\t' + "%.4f" % confusion_matrix[1][1])
