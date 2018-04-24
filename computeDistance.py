import csv, math, os, os.path, random
from datetime import datetime
from argparse import ArgumentParser
from multiprocessing import Process, Array
from utils import parallel
from utils import general_utils as gu
from utils import io_utils
from comparators.ComparatorFactory import ComparatorFactory

PAIR_ID_COL = 1
QUESTION1_COL = 2
QUESTION2_COL = 3


def write_results(file_name, questions, distances):
    with open(file_name, 'a') as results_file:
        writer = csv.writer(results_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for i, row in enumerate(questions):
            file_line = [row[PAIR_ID_COL], "%.4f" % distances[i]]
            writer.writerow(file_line)


def distribute_comparing_work(questions, distances, num_workers, comparator):
    total = len(questions)
    matrix_size = math.ceil(total / num_workers)
    index_from = 0
    index_to = matrix_size

    workers = []
    for i in range(num_workers):
        if index_from >= total:
            break

        worker = Process(target=parallel.compare_pairs,
                         args=(questions[index_from:index_to], distances, comparator, QUESTION1_COL, QUESTION2_COL))
        worker.start()
        workers.append(worker)

        index_from += matrix_size
        index_to += matrix_size if index_to + matrix_size <= total else total

    # Waits until the workers finish their work
    for worker in workers:
        worker.join()


def define_first_row(previous_path):
    first_row = 0

    if previous_path is not None:
        with open(previous_path) as previous_runs:
            reader = csv.reader(previous_runs)
            next(reader)  # Ignores the header

            for _ in reader:
                first_row += 1

    return first_row


def create_file(technique, previous_path, result_path):
    if not previous_path:
        results_path = os.path.join(result_path, 'computeDistance_' + technique + '_' + '{:%Y%m%d_%H%M%S}'.format(datetime.now()) + '.csv')

        with open(results_path, 'w') as results_file:
            writer = csv.writer(results_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['pair_id', 'distance'])

        return results_path
    else:
        return previous_path


def save_sample_file(questions_data, questions_size, sample_path):
    sample_full_path = os.path.join(sample_path, 'question_pairs_subset_' + str(questions_size) + ".csv")
    io_utils.write_csv_file(sample_full_path, questions_data)


def read_csv_file(quora_file_path, questions_size, sample_path):
    """
    Returns a random subset from the complete set of questions, applying a random sample.

    :param quora_file_path: csv file which contains all the questions.
    :param questions_size: subset size.
    :param sample_path: path where the sample file will be saved.
    :return: two arrays which contains a subset of questions.
    """
    all_questions = []
    questions = []

    with open(quora_file_path, 'r') as questions_file:
        reader = csv.reader(questions_file)
        for i, row in enumerate(reader):
            all_questions.append(row)

    # Random sample only if questions_size is not zero.
    questions_data = all_questions if not questions_size else random.sample(all_questions, questions_size)
    save_sample_file(questions_data, questions_size, sample_path)

    for i, row in enumerate(questions_data):
        questions_data[i] = [i] + row
        questions.append(row[QUESTION1_COL - 1])
        questions.append(row[QUESTION2_COL - 1])

    return questions, questions_data


def start_comparison(technique, quora_file_path, num_workers, previous_path, questions_size, results_path, batch_size):
    gu.print_screen('Loading file...')

    io_utils.create_directory(results_path)

    questions, questions_data = read_csv_file(quora_file_path, questions_size, results_path)
    comparator = ComparatorFactory().get_comparator(technique, questions)

    file_name = create_file(technique, previous_path, results_path)
    current_batch = define_first_row(previous_path)

    total_questions_count = len(questions_data)
    distances = Array('f', total_questions_count)

    while current_batch < total_questions_count:
        total = batch_size if (current_batch + batch_size <= total_questions_count) else (
            total_questions_count - current_batch)
        end_batch = current_batch + total

        distribute_comparing_work(questions_data[current_batch:end_batch], distances, num_workers, comparator)
        write_results(file_name, questions_data[current_batch:end_batch], distances[current_batch:end_batch])

        gu.print_screen('First ' + str(end_batch) + ' distances calculated.')

        current_batch += batch_size

    gu.print_screen('Script finished. Total time: ' + str(datetime.now() - start_time))


if __name__ == '__main__':
    start_time = datetime.now()
    gu.print_screen('Starting script.')

    parser = ArgumentParser('Computes the distance of each pair')

    parser.add_argument('-t', dest='technique', required=True, choices=['bow', 'tfidf', 'gtfidf', 'w2v', 'ft', 'sem'], help='Comparison technique (required)')
    parser.add_argument('-q', dest='quora_path', required=True, help='Quora data set path (required)')
    parser.add_argument('-w', dest='number_workers', default=5, type=int, help='Number of parallel processes [default = 5]')
    parser.add_argument('-b', dest='batch_size', default=500, type=int, help='Batch size')
    parser.add_argument('-n', dest='questions_size', default=0, type=int, help='Questions subset size that will be processed (0 -> all the questions)')
    parser.add_argument('-results_path', dest='results_path', default='/tmp', help='Path where the result files will be saved')
    parser.add_argument('-previous', dest='previous_path', help='Previous results file path (when you need to resume an unfinished experiment)')
    args = parser.parse_args()

    start_comparison(args.technique,
                     args.quora_path,
                     args.number_workers,
                     args.previous_path,
                     args.questions_size,
                     args.results_path,
                     args.batch_size)
