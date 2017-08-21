import csv, math, os, os.path
from datetime import datetime
from argparse import ArgumentParser
from multiprocessing import Process, Array
from utils import parallel
from utils import general_utils as gu
from comparators.ComparatorFactory import ComparatorFactory

PAIR_ID_COL = 1
QUESTION1_COL = 2
QUESTION2_COL = 3


def define_first_row(previous_path):
    first_row = 0

    if previous_path is not None:
        with open(previous_path) as previous_runs:
            reader = csv.reader(previous_runs)
            next(reader)  # Ignores the header

            for row in reader:
                first_row += 1

    return first_row


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


def create_file(previous_path):
    if previous_path is None:
        if not os.path.exists('results'):
            os.mkdir('results')

        results_path = os.path.join('results', 'computeDistance_'
                        + technique + '_' + '{:%Y%m%d_%H%M%S}'.format(datetime.now()) + '.csv')

        with open(results_path, 'w') as results_file:
            writer = csv.writer(results_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['pair_id', 'distance'])

        return results_path
    else:
        return previous_path


def write_results(file_name, questions, distances):
    with open(file_name, 'a') as results_file:
        writer = csv.writer(results_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for i, row in enumerate(questions):
            file_line = []
            file_line.append(row[PAIR_ID_COL])
            file_line.append("%.4f" % distances[i])

            writer.writerow(file_line)

if __name__ == '__main__':
    start_time = datetime.now()
    gu.print_screen('Starting script.')

    parser = ArgumentParser('Computes the distance of each pair')

    parser.add_argument('-t', dest='technique',      required=True, choices=['bow', 'tfidf', 'gtfidf', 'w2v', 'ft', 'sem'])
    parser.add_argument('-q', dest='quora_path',     required=True)
    parser.add_argument('-w', dest='number_workers', default=5, type=int)

    parser.add_argument('-previous',  dest='previous_path')

    args = parser.parse_args()
    technique = args.technique
    quora_path = args.quora_path
    num_workers = args.number_workers
    previous_path = args.previous_path

    gu.print_screen('Loading file...')

    questions_data = []
    questions = []
    with open(quora_path, 'r') as questions_file:
        reader = csv.reader(questions_file)

        next(reader)
        for i, row in enumerate(reader):
            questions_data.append([i] + row)
            questions.append(row[QUESTION1_COL - 1])
            questions.append(row[QUESTION2_COL - 1])

    total_questions = len(questions_data)

    factory = ComparatorFactory()
    comparator = factory.get_comparator(technique, questions)

    file_name = create_file(previous_path)

    distances = Array('f', total_questions)

    start_batch = define_first_row(previous_path)
    batch_size = 500

    while start_batch < total_questions:
        total = batch_size if (start_batch + batch_size <= total_questions) else (total_questions - start_batch)
        end_batch = start_batch + total

        distribute_comparing_work(questions_data[start_batch:end_batch], distances, num_workers, comparator)

        write_results(file_name, questions_data[start_batch:end_batch], distances[start_batch:end_batch])

        gu.print_screen('First ' + str(end_batch) + ' distances calculated.')

        start_batch += batch_size

    gu.print_screen('Script finished. Total time: ' + str(datetime.now() - start_time))