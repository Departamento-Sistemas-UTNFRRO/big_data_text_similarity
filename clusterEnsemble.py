from argparse import ArgumentParser
from datetime import datetime

import math, uuid
from ensembles.clustering.pam_helper import PamHelper
from ensembles.comparators.comparator_factory import ComparatorFactory
from utils import general_utils as gu
from ensembles.dao import ensembles_dao
from ensembles import distance_matrix_builder
from ensembles import clustering_ensembler
from ensembles.spark.spark_helper import create_spark_session
from utils.io_utils import get_current_result_path, build_question_path, get_or_create_experiment_path, copy_pair_file_to_experiment_folder
from multiprocessing import Process

spark = create_spark_session()


def generate_ensembles(techniques, base_input_path, samples_number, results_path, sample_size, k, clustering_runs,
                       in_progress_experiment_path, calc_distances_enabled, clustering_enabled, ensembles_enabled, start_from_sample_num):
    experiment_path = get_or_create_experiment_path(results_path, sample_size, samples_number, k, clustering_runs, in_progress_experiment_path)
    gu.print_screen('Starting experiments in the path: ' + experiment_path)
    for run in range(start_from_sample_num, samples_number + 1):
        gu.print_screen('----- Run number ' + str(run) + ' ------')
        current_result_path = get_current_result_path(experiment_path, sample_size, run)
        questions_path = build_question_path(base_input_path, sample_size, run)
        sample_individual_questions = load_questions_sample(questions_path, sample_size, current_result_path)

        gu.print_screen('Getting triangular matrix')
        triangular_matrix = distance_matrix_builder.get_triangular_matrix(sample_individual_questions)
        triangular_matrix.persist()

        for technique in techniques.split(','):
            distance_matrix = []
            if calc_distances_enabled:
                distance_matrix = calculate_distances(technique, sample_individual_questions, triangular_matrix, calc_distances_enabled)
                distance_matrix.persist()
                ensembles_dao.write_distance_matrix_to_file(distance_matrix, current_result_path, technique)
            else:
                if clustering_enabled:
                    gu.print_screen('Distances calculation disabled.')
                    distance_matrix = ensembles_dao.get_distance_matrix_from_files(spark, current_result_path, technique)

            if clustering_enabled:
                generate_clustering_labels(sample_size, sample_individual_questions, distance_matrix, current_result_path, k, clustering_runs)

        if ensembles_enabled:
            generate_coasociation_matrix(sample_individual_questions, triangular_matrix, current_result_path)


def load_questions_sample(questions_path, sample_size, results_path):
    gu.print_screen('Getting sample as DF [sequential_id, pair_id, question_1, question_2, duplicate_indicator]')
    sample = ensembles_dao.get_questions_from_sample(spark, questions_path)
    copy_pair_file_to_experiment_folder(questions_path, results_path)

    gu.print_screen('Getting individual questions from pairs as DF [sequential_id, question]')
    sample_individual_questions = distance_matrix_builder.get_individual_questions_from_pairs(sample, sample_size)
    sample_individual_questions.persist()
    ensembles_dao.write_individiual_questions(sample_individual_questions, results_path)

    return sample_individual_questions


def calculate_distances(technique, sample_individual_questions, triangular_matrix, calc_distances_enabled):
    if calc_distances_enabled:
        gu.print_screen('Calculating distances with technique: ' + technique + '. Result RDD[question_1, question_2, distance]')

        questions_for_training = sample_individual_questions \
            .select('question') \
            .rdd \
            .flatMap(lambda x: x) \
            .collect()
        comparator = ComparatorFactory().get_comparator(technique, questions_for_training)
        return distance_matrix_builder.build(spark, technique, triangular_matrix, comparator)


def generate_clustering_labels(sample_size, sample_individual_questions, similarity_matrix, current_results_path, k, clustering_runs):
    n = sample_size * 2  # The sample size of the individual questions DS.

    # Collecting everything to master. See if we can avoid this step (maybe using an intermediate file).
    sample_individual_questions_array = sample_individual_questions.collect()
    similarity_matrix_dict = similarity_matrix \
        .toPandas() \
        .set_index(['sequential_id_1', 'sequential_id_2']) \
        .T \
        .to_dict()

    similarity_matrix.unpersist()
    gu.print_screen('Generating clustering labels.')
    execute_parallel_clustering(sample_individual_questions_array, similarity_matrix_dict, n, current_results_path, k, clustering_runs)


def execute_parallel_clustering(sample_individual_questions_array, distance_matrix_dict, n, current_result_path, k, clustering_runs):
    workers = []
    k_array = [k] * clustering_runs
    num_workers = 8
    k_array_chunks = list(chunks(k_array, num_workers))

    for k_chunk in k_array_chunks:
        pam_helper = PamHelper(n, k_chunk)
        worker = Process(target=pam_helper.generate_clustering_labels_for_k,
                         args=(sample_individual_questions_array, distance_matrix_dict, current_result_path))
        worker.start()
        workers.append(worker)

    for worker in workers:
        worker.join()


def chunks(lst, workers):
    n = math.ceil(len(lst) / workers)
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def execute_serial_clustering(sample_individual_questions_array, distance_matrix_dict, n, current_result_path, k, clustering_runs):
    k_array = [k] * clustering_runs
    pam_helper = PamHelper(n, k_array)
    pam_helper.generate_clustering_labels_for_k(sample_individual_questions_array, distance_matrix_dict, current_result_path)


def generate_coasociation_matrix(sample_individual_questions, triangular_matrix, current_result_path):
    coassociation_matrix = clustering_ensembler.generate_coassociation_matrix(spark, sample_individual_questions, triangular_matrix, current_result_path)
    ensembles_dao.write_coassociation_matrix(coassociation_matrix, current_result_path)


if __name__ == '__main__':
    start_time = datetime.now()
    gu.print_screen('Starting script.')

    parser = ArgumentParser('Computes the distance of each pair')

    parser.add_argument('-techniques', dest='techniques',
                        help='Comma list separated of techniques. Full list: bow,tfidf,gtfidf,w2v,ft,sem.')
    parser.add_argument('-questions_path', dest='questions_path', required=True,
                        help='Input question pair data set path (required)')
    parser.add_argument('-sample_size', dest='sample_size', default=0, type=int, help='Questions set size.')
    parser.add_argument('-samples_number', dest='samples_number', required=True, default=1, type=int,
                        help='Numbers of samples that are going to be taken in loop.')
    parser.add_argument('-results_path', dest='results_path', default='/Users/ftesone/Documents/Tesis/experiments',
                        help='Path where the result files will be saved')
    parser.add_argument('-k', dest='k', default=1, type=int, help='Number of clusters (medoids)')
    parser.add_argument('-clustering_runs', dest='clustering_runs', default=1, type=int, help='Number of PAM clustering runs.')
    parser.add_argument('-in_progress_experiment_path', dest='in_progress_experiment_path', default='', help='If null, creates a new folder the results.')
    parser.add_argument('-calc_distances_enabled', dest='calc_distances_enabled', action='store_true', default=False)
    parser.add_argument('-clustering_enabled', dest='clustering_enabled', action='store_true', default=False)
    parser.add_argument('-ensemble_enabled', dest='ensemble_enabled', action='store_true', default=False)
    parser.add_argument('-start_from_sample_num', dest='start_from_sample_num', default=1, type=int, help='Sample number to start from.')

    args = parser.parse_args()

    generate_ensembles(args.techniques,
                       args.questions_path,
                       args.samples_number,
                       args.results_path,
                       args.sample_size,
                       args.k,
                       args.clustering_runs,
                       args.in_progress_experiment_path,
                       args.calc_distances_enabled,
                       args.clustering_enabled,
                       args.ensemble_enabled,
                       args.start_from_sample_num)

    gu.print_screen('Script finished. Total time: ' + str(datetime.now() - start_time))
