import csv
import math
import os
import os.path
import config
from datetime import datetime
from argparse import ArgumentParser
from multiprocessing import Process, Array
from utils import parallel
from utils import general_utils as gu
from utils import io_utils
from utils import question_sampler as sampler
from comparators.ComparatorFactory import ComparatorFactory

PAIR_ID_COL = config.quora_file.get('pair_id') + 1
QUESTION1_COL = config.quora_file.get('question1') + 1
QUESTION2_COL = config.quora_file.get('question2') + 1

logger = gu.get_logger(__name__)


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


def create_file(technique, previous_path, result_path, run, run_time):
    if not previous_path:
        results_path = os.path.join(result_path, 'computeDistance_' + technique + '_' + str(run) + '_' + '{:%Y%m%d_%H%M%S}'.format(run_time) + '.csv')

        with open(results_path, 'w') as results_file:
            writer = csv.writer(results_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['pair_id', 'distance'])

        return results_path
    else:
        return previous_path


def get_existing_sample(sample_path, sample_file_name, run_number):
    file_name = sample_path + sample_file_name + '_' + str(run_number) + '.csv'

    logger.info('Reading sample file ' + file_name)

    with open(file_name, 'r') as sample_file:
        reader = csv.reader(sample_file)

        questions = []
        questions_data = []
        for row in reader:
            row[0] = int(row[PAIR_ID_COL])

            questions.append(row[QUESTION1_COL])
            questions.append(row[QUESTION2_COL])
            questions_data.append(row)

    return questions, questions_data


def start(technique, quora_file_path, num_workers, previous_path, questions_size, results_path, batch_size, runs_number,
          sample_path, sample_file_name):
    start_time = datetime.now()
    logger.info('Starting script.')

    all_questions = io_utils.read_quora_csv_file(quora_file_path)

    for run in range(1, runs_number + 1):
        logger.info('----- Run number ' + str(run) + ' ------')

        if sample_file_name:
            questions, questions_data = get_existing_sample(sample_path, sample_file_name, run)
        else:
            questions, questions_data = sampler.generate_sample(all_questions, questions_size, sample_path, run)

        comparator = ComparatorFactory().get_comparator(technique, questions)

        file_name = create_file(technique, previous_path, results_path, run, start_time)
        current_batch = gu.define_first_row(previous_path)

        total_questions_count = len(questions_data)
        distances = Array('f', total_questions_count)

        while current_batch < total_questions_count:
            total = batch_size if (current_batch + batch_size <= total_questions_count) else (total_questions_count - current_batch)
            end_batch = current_batch + total

            distribute_comparing_work(questions_data[current_batch:end_batch], distances, num_workers, comparator)
            write_results(file_name, questions_data[current_batch:end_batch], distances[current_batch:end_batch])

            logger.info('First ' + str(end_batch) + ' distances calculated.')

            current_batch += batch_size

        logger.info('Script finished. Total time: ' + str(datetime.now() - start_time))


if __name__ == '__main__':
    parser = ArgumentParser('Computes the distance of each pair')

    parser.add_argument('-t', dest='technique', required=True, choices=['bow', 'tfidf', 'gtfidf', 'w2v', 'ft', 'sem'], help='Comparison technique (required)')
    parser.add_argument('-q', dest='quora_path', required=True, help='Quora data set path (required)')
    parser.add_argument('-w', dest='number_workers', default=5, type=int, help='Number of parallel processes [default = 5]')
    parser.add_argument('-previous', dest='previous_path', help='Previous results file path (when you need to resume an unfinished experiment)')
    parser.add_argument('-n', dest='questions_size', default=0, type=int, help='Questions subset size that will be processed (0 -> all the questions)')
    parser.add_argument('-b', dest='batch_size', default=500, type=int, help='Batch size')
    parser.add_argument('-runs', dest='runs', default=1, type=int, help='Total runs number')
    parser.add_argument('-results_path', dest='results_path', default='/tmp', help='Path where the result files will be saved')
    parser.add_argument('-sample', dest='sample_path', help='Path to sample file (if not provided, creates a new sample)')
    parser.add_argument('-sname', dest='sample_file_name', help='First part of the sample file name (the string _runnumber.csv will be appended)')

    args = parser.parse_args()

    start(args.technique,
          args.quora_path,
          args.number_workers,
          args.previous_path,
          args.questions_size,
          args.results_path,
          args.batch_size,
          args.runs,
          args.sample_path,
          args.sample_file_name)
