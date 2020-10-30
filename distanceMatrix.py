import csv, math, os.path
from datetime import datetime
from argparse import ArgumentParser
from multiprocessing import Process, Array
from utils import parallel
from utils import general_utils as gu
from utils import io_utils
from comparators.ComparatorFactory import ComparatorFactory

QUESTION1_COL = 2
QUESTION2_COL = 3


def distribute_comparing_work(question, questions, distances, num_workers, comparator):
    total = len(questions)
    matrix_size = math.ceil(total / num_workers)
    index_from = 0
    index_to = matrix_size

    workers = []
    for i in range(num_workers):

        worker = Process(target=parallel.compare_question,
                         args=(question, questions[index_from:index_to], distances, comparator))
        worker.start()
        workers.append(worker)

        index_from += matrix_size
        index_to += matrix_size if index_to + matrix_size <= total else total

    # Waits until the workers finish their work
    for worker in workers:
        worker.join()


if __name__ == '__main__':
    start_time = datetime.now()
    gu.print_screen('Starting script.')

    parser = ArgumentParser('Computes the distance between all the questions')

    parser.add_argument('-t', dest='technique', required=True,
                        choices=['cos', 'tfidf', 'gtfidf', 'w2v', 'ft', 'sem', 'ens'])
    # parser.add_argument('-q', dest='quora_path', required=True)
    parser.add_argument('-runs', dest='runs', default=1, type=int, help='Total runs number')
    parser.add_argument('-input_path', dest='input_path', default='/tmp',
                        help='Path where the samples and distances files will be saved')
    parser.add_argument('-n', dest='sample_size', default=0, type=int,
                        help='Questions subset size that will be processed (0 -> all the questions)')

    parser.add_argument('-w', dest='number_workers', default=5, type=int)

    args = parser.parse_args()
    technique = args.technique
    # quora_path = args.quora_path
    runs = args.runs
    input_path = args.input_path
    sample_size = args.sample_size
    num_workers = args.number_workers

    # Creates result directory
    if not os.path.exists('results'):
        os.mkdir('results')

    for run in range(1, runs + 1):
        gu.print_screen('Loading file...')
        sample_questions = io_utils.read_sample_file(input_path, sample_size, run)

        questions = [] # Gets the questions to train the comparator
        index_questions = [] # Questions with index to parallelize
        i = 0
        for question_row in sample_questions:
            # Question 1
            questions.append(question_row[QUESTION1_COL])
            index_questions.append([i] + question_row[QUESTION1_COL:QUESTION1_COL + 1])
            i += 1

            # Question 2
            questions.append(question_row[QUESTION2_COL])
            index_questions.append([i] + question_row[QUESTION2_COL:QUESTION2_COL + 1])
            i += 1

        factory = ComparatorFactory()
        comparator = factory.get_comparator(technique, questions)

        results_path = os.path.join('results', 'distanceMatrix_'
                                    + technique + '_' + str(run) + '_'
                                    + '{:%Y%m%d_%H%M%S}'.format(datetime.now()) + '.csv')

        with open(results_path, 'w') as results_file:
            writer = csv.writer(results_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for i, row in enumerate(index_questions):
                gu.print_screen('Comparing ' + str(i + 1) + ' of ' + str(sample_size * 2))

                distances = Array('f', len(index_questions))

                question = row[1]
                distribute_comparing_work(question, index_questions, distances, num_workers, comparator)

                writer.writerow([distance for distance in distances])

        gu.print_screen("Run " + str(run) + " finished")
