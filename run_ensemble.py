from argparse import ArgumentParser
from datetime import datetime

import compute_distance
import confusion_matrix
import pre_process_questions as pre_process
from utils import general_utils as gu
from utils import io_utils

logger = gu.get_logger(__name__)


def start(pre_processing,
          technique,
          quora_file_path,
          raw_quora_file_path,
          num_workers,
          previous_path,
          questions_size,
          results_path,
          batch_size,
          runs_number,
          sample_path,
          sample_file_name):
    logger.info('Starting ensemble calculation.')
    start_time = datetime.now()

    # Pre-process questions.
    if pre_processing:
        pre_process.start(raw_quora_file_path, quora_file_path)

    distances_path = io_utils.create_date_path(results_path, start_time)
    sample_date_path = io_utils.create_date_path(sample_path, start_time)

    # Create distances files.
    compute_distance.start(technique,
                           quora_file_path,
                           num_workers,
                           previous_path,
                           questions_size,
                           distances_path,
                           batch_size,
                           runs_number,
                           sample_date_path,
                           sample_file_name)

    # Calculate confusion matrix.
    confusion_matrix.start(technique, runs_number, distances_path, questions_size, sample_date_path)

    logger.info('Ensemble calculation finished. Total time: ' + str(datetime.now() - start_time))


if __name__ == '__main__':
    parser = ArgumentParser('Computes the distance of each pair')

    parser.add_argument('-pre-processing', dest='pre_processing', default=False, help='Apply pre-processing to the raw quora file.')

    parser.add_argument('-t', dest='technique', required=True, choices=['bow', 'tfidf', 'gtfidf', 'w2v', 'ft', 'sem'], help='Comparison technique (required)')

    # File configs.
    parser.add_argument('-q', dest='quora_path', default='data/question_pairs.csv',
                        help='Path where the pre-processed file will be saved')
    parser.add_argument('-raw-quora-path', dest='raw_quora_path', default='data/quora_duplicate_questions.tsv',
                        help='Quora data set path without pre-processing')
    parser.add_argument('-previous-path', dest='previous_path',
                        help='Previous results file path (when you need to resume an unfinished experiment)')
    parser.add_argument('-distances-path', dest='results_path', default='/tmp/distances',
                        help='Path where the result files will be saved')
    parser.add_argument('-samples-path', dest='sample_path', default='/tmp/samples',
                        help='Path to sample file (if not provided, creates a new sample)')
    parser.add_argument('-sname', dest='sample_file_name',
                        help='First part of the sample file name (the string _runnumber.csv will be appended)')

    # Run configs.
    parser.add_argument('-w', dest='number_workers', default=5, type=int, help='Number of parallel processes [default = 5]')
    parser.add_argument('-n', dest='questions_size', default=0, type=int, help='Questions subset size that will be processed (0 -> all the questions)')
    parser.add_argument('-b', dest='batch_size', default=500, type=int, help='Batch size')
    parser.add_argument('-runs', dest='runs', default=1, type=int, help='Total runs number')

    args = parser.parse_args()

    start(args.pre_processing,
          args.technique,
          args.quora_path,
          args.raw_quora_path,
          args.number_workers,
          args.previous_path,
          args.questions_size,
          args.results_path,
          args.batch_size,
          args.runs,
          args.sample_path,
          args.sample_file_name)
