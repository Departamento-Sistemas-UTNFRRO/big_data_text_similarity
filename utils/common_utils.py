import math
import numpy as np
from multiprocessing import Process
from utils import parallel

QUESTION1_COL = 1
QUESTION2_COL = 2
DUPLICATE_COL = 3


def prepare_relations(pair_ids, data_questions):
    question_pairs = []
    relations = np.zeros([len(pair_ids)])  # Vector with quora relations

    for i, pair_id in enumerate(pair_ids):
        question_pairs.append([
            i,  # Line number (general level)
            data_questions[pair_id][QUESTION1_COL],
            data_questions[pair_id][QUESTION2_COL]
        ])

        relations[i] = np.array(int(data_questions[pair_id][DUPLICATE_COL]))

    return question_pairs, relations


def distribute_comparing_work(question_pairs, distances, num_workers, comparator):
    total = len(question_pairs)
    matrix_size = math.ceil(total / num_workers)
    index_from = 0
    index_to = matrix_size

    q1_col = 1
    q2_col = 2

    workers = []
    for i in range(num_workers):
        worker = Process(target=parallel.compare_pairs,
                         args=(question_pairs[index_from:index_to], distances, comparator, q1_col, q2_col))
        worker.start()
        workers.append(worker)

        index_from += matrix_size
        index_to += matrix_size if index_to + matrix_size <= total else total

    # Waits until the workers finish their work
    for worker in workers:
        worker.join()


def find_best_threshold(relations, distances, num_pairs):
    min_threshold = 0.05
    max_threshold = 1
    step = 0.05

    precisions = np.array([[threshold, 0.] for threshold in np.arange(min_threshold, max_threshold, step)])

    for precision_row in precisions:
        precision_row[1] = compute_precision(relations, distances, precision_row[0], num_pairs)

    # When there is more than one optimal threshold, picks one randomly
    max_precision = np.amax(precisions[:, 1])
    max_indices = np.argwhere(precisions[:, 1] == max_precision)
    max_indices = max_indices.reshape(max_indices.shape[0])

    return precisions[np.random.choice(max_indices)][0]


def compute_validation_error(relations, distances, threshold, num_pairs):
    precision = compute_precision(relations, distances, threshold, num_pairs)

    return 1 - precision


def compute_precision(relations, distances, threshold, num_pairs):
    return (relations[:num_pairs] == [distances[i] <= threshold for i in range(num_pairs)]).mean()
