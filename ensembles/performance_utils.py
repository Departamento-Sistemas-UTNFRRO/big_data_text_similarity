import numpy as np


def find_best_threshold(relations, similarities, num_pairs):
    min_threshold = 0.001
    max_threshold = 1
    step = 0.001

    precisions = np.array([[threshold, 0.] for threshold in np.arange(min_threshold, max_threshold, step)])

    for precision_row in precisions:
        precision_row[1] = compute_precision(relations, similarities, precision_row[0], num_pairs)

    # When there is more than one optimal threshold, picks one randomly
    max_precision = np.amax(precisions[:, 1])
    max_indices = np.argwhere(precisions[:, 1] == max_precision)
    max_indices = max_indices.reshape(max_indices.shape[0])

    return precisions[np.random.choice(max_indices)][0]


def compute_validation_error(relations, distances, threshold, num_pairs):
    precision = compute_precision(relations, distances, threshold, num_pairs)

    return 1 - precision


def compute_precision(relations, similarities, threshold, num_pairs):
    return (relations[:num_pairs] == [similarities[i] >= threshold for i in range(num_pairs)]).mean()
