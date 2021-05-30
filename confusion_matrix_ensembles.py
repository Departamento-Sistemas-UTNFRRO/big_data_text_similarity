import os.path
from argparse import ArgumentParser
from datetime import datetime
from ensembles.dao import ensembles_dao
from ensembles.spark.spark_helper import create_spark_session
from pyspark.sql.types import StructType, StructField, IntegerType
from ensembles import performance_utils as pu
import numpy as np

from utils import general_utils as gu
from utils import io_utils

spark = create_spark_session()

pairs_schema = StructType([StructField("question_id_1", IntegerType(), True),
                           StructField("question_id_2", IntegerType(), True)])


def calculate_confusion_matrix(runs, sample_size, experiment_path):
    confusion_matrix_array = []
    threshold_array = []
    error_array = []

    for run in range(1, runs + 1):
        confusion_matrix, threshold, error = create_confusion_matrix_for_run(run, sample_size, experiment_path)
        confusion_matrix_array.append(confusion_matrix)
        threshold_array.append(threshold)
        error_array.append(error)

    generate_report(runs, sample_size, experiment_path, confusion_matrix_array, threshold_array, error_array)
    gu.print_screen('Script finished. Total time: ' + str(datetime.now() - start_time))


def create_confusion_matrix_for_run(run, sample_size, experiment_path):
    sample_questions = get_sample_questions(experiment_path, sample_size, run)

    n = sample_size if sample_size else len(sample_questions)
    coassociation_matrix = get_coassociation_matrix(experiment_path, sample_size, run)
    similarities = get_input_pairs_from_coassociation_matrix(coassociation_matrix, n).collect()

    real_relations = np.zeros(n)
    pair_similarities = []
    for i in range(n):
        real_relations[i] = int(sample_questions[i][4])
        pair_similarities.append(float(similarities[i][4]))

    threshold = pu.find_best_threshold(real_relations, pair_similarities, n)
    error = pu.compute_validation_error(real_relations, pair_similarities, threshold, n)

    gu.print_screen('Threshold used in confusion matrix: ' + str(threshold))
    confusion_matrix = build_confusion_matrix(real_relations, pair_similarities, threshold)

    return confusion_matrix, threshold, error


def get_sample_questions(experiment_path, sample_size, run):
    pairs_path = os.path.join(get_current_experiment_path(experiment_path, sample_size, run), 'pairs')
    sample_questions_path = io_utils.build_question_path(pairs_path, sample_size, run)
    return io_utils.read_csv_file(sample_questions_path)


def get_coassociation_matrix(experiment_path, sample_size, run):
    coassociation_matrix_path = get_current_experiment_path(experiment_path, sample_size, run)
    return ensembles_dao.get_coassociation_matrix(spark, coassociation_matrix_path)


def get_current_experiment_path(experiment_path, sample_size, run):
    return os.path.join(experiment_path, str(sample_size) + '_' + str(run))


def get_input_pairs_from_coassociation_matrix(coassociation_matrix, n):
    pairs = []
    for i in range(0, n):
        pairs.append((i, i + n))

    input_pairs_df = spark.createDataFrame(pairs, pairs_schema)
    return input_pairs_df \
        .join(coassociation_matrix, ['question_id_1', 'question_id_2']) \
        .orderBy(["question_id_1", "question_id_2"], ascending=[1, 1])


def build_confusion_matrix(real_relations, pair_similarities, threshold):
    confusion_matrix = [[0, 0], [0, 0]]

    guessed_relations = np.array([1 if pair_similarities[i] >= threshold else 0 for i in range(len(real_relations))])

    confusion_matrix[0][0] = ((real_relations == 0) * (guessed_relations == 0)).mean()
    confusion_matrix[0][1] = ((real_relations == 0) * (guessed_relations == 1)).mean()
    confusion_matrix[1][0] = ((real_relations == 1) * (guessed_relations == 0)).mean()
    confusion_matrix[1][1] = ((real_relations == 1) * (guessed_relations == 1)).mean()

    return confusion_matrix


def generate_report(runs, sample_size, experiment_path, confusion_matrix_array, threshold_array, error_array):
    # Writes threshold and errors in a file
    header = """Clustering ensemble results
    Samples size: {0}
    Number of runs: {1}
    
    Samples: \n\n""".format(sample_size, runs)

    body = ''
    sum_cf_precision = 0
    sum_cf_error = 0
    total_confusion_matrix = [[0, 0], [0, 0]]

    error_report_content = ""
    for run in range(0, runs):
        confusion_matrix = confusion_matrix_array[run]
        sample_header = "\n\nSample number {0} \n".format(run + 1)
        confusion_matrix_string = "Confusion Matrix: \n"
        confusion_matrix_first_line = '\t' + "%.4f" % confusion_matrix[0][0] + '\t' + "%.4f" % confusion_matrix[0][1] + "\n"
        confusion_matrix_second_line = '\t' + "%.4f" % confusion_matrix[1][0] + '\t' + "%.4f" % confusion_matrix[1][1] + "\n"
        cf_precision = confusion_matrix[0][0] + confusion_matrix[1][1]
        cf_error = confusion_matrix[0][1] + confusion_matrix[1][0]
        sum_line = 'Precision {0} - Error {1}'.format(cf_precision, cf_error) + "\n"
        threshold_line = 'Threshold: {0}'.format(threshold_array[run]) + "\n"
        error_line = 'Error: {0}'.format(error_array[run]) + "\n"

        body += sample_header + confusion_matrix_string + confusion_matrix_first_line + confusion_matrix_second_line + sum_line + threshold_line + error_line

        sum_cf_precision += cf_precision
        sum_cf_error += cf_precision
        total_confusion_matrix[0][0] += confusion_matrix[0][0]
        total_confusion_matrix[0][1] += confusion_matrix[0][1]
        total_confusion_matrix[1][0] += confusion_matrix[1][0]
        total_confusion_matrix[1][1] += confusion_matrix[1][1]

        error_report_content += 'ensemble,' + str(sample_size) + "," + str(confusion_matrix[0][1] + confusion_matrix[1][0]) + "\n"

    total_confusion_matrix[0][0] = total_confusion_matrix[0][0] / runs
    total_confusion_matrix[0][1] = total_confusion_matrix[0][1] / runs
    total_confusion_matrix[1][0] = total_confusion_matrix[1][0] / runs
    total_confusion_matrix[1][1] = total_confusion_matrix[1][1] / runs

    total_confusion_matrix_string = "\n\n **************** Total Confusion Matrix: **************** \n"
    total_confusion_matrix_first_line = '\t' + "%.4f" % total_confusion_matrix[0][0] + '\t' + "%.4f" % total_confusion_matrix[0][1] + "\n"
    total_confusion_matrix_second_line = '\t' + "%.4f" % total_confusion_matrix[1][0] + '\t' + "%.4f" % total_confusion_matrix[1][1] + "\n"
    total_cf_precision = total_confusion_matrix[0][0] + total_confusion_matrix[1][1]
    total_cf_error = total_confusion_matrix[0][1] + total_confusion_matrix[1][0]
    total_sum_line = 'Precision {0} - Error {1}'.format(total_cf_precision, total_cf_error) + "\n"
    results_line = total_confusion_matrix_string + total_confusion_matrix_first_line + total_confusion_matrix_second_line + total_sum_line

    report = header + body + results_line

    with open(experiment_path + '/report_new.txt', "w") as file_report:
        file_report.writelines(report)

    error_report_content += 'ensemble,' + str(sample_size) + "," + str(total_confusion_matrix[0][1] + total_confusion_matrix[1][0])
    with open(experiment_path + '/error_report.txt', "w") as file_report:
        file_report.writelines(error_report_content)


if __name__ == '__main__':
    start_time = datetime.now()

    gu.print_screen('Starting script.')

    parser = ArgumentParser('Computes the confusion matrix of a comparison technique')

    parser.add_argument('-runs', dest='runs', default=1, type=int, help='Total runs number', required=True)
    parser.add_argument('-sample_size', dest='sample_size', default=0, type=int,
                        help='Questions subset size that will be processed (0 -> all the questions)', required=True)
    parser.add_argument('-experiment_path', dest='experiment_path', default='/tmp', help='Path where the experiment was stored', required=True)

    args = parser.parse_args()

    calculate_confusion_matrix(args.runs, args.sample_size, args.experiment_path)
