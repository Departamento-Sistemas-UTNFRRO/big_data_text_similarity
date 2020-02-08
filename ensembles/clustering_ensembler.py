from ensembles.dao import ensembles_dao
from pyspark.sql.functions import count, lit, sum, collect_list, struct, udf
from utils import io_utils
from utils import general_utils as gu
from pyspark.sql.types import FloatType


def generate_coassociation_matrix(spark, sample_individual_questions, triangular_matrix, results_path):
    total_runs = io_utils.get_number_of_files_in_dir(results_path + '/labels')
    gu.print_screen('Running ensemble. Numbers of runs: ' + str(total_runs))
    all_labels = ensembles_dao.get_clustering_labels(spark, results_path)

    coassociation_matrix = build_coassociation_matrix(all_labels, triangular_matrix, total_runs)

    sample_individual_questions_1 = sample_individual_questions \
        .withColumnRenamed('sequential_id', 'sequential_id_1') \
        .withColumnRenamed('question', 'question_1')

    sample_individual_questions_2 = sample_individual_questions \
        .withColumnRenamed('sequential_id', 'sequential_id_2') \
        .withColumnRenamed('question', 'question_2')

    sample_individual_questions.unpersist()

    return coassociation_matrix \
        .join(sample_individual_questions_1, coassociation_matrix.question_id_1 == sample_individual_questions_1.sequential_id_1) \
        .join(sample_individual_questions_2, coassociation_matrix.question_id_2 == sample_individual_questions_2.sequential_id_2) \
        .select('question_id_1', 'question_id_2', 'question_1', 'question_2', 'similarity')


def build_coassociation_matrix(all_labels, triangular_matrix, total_runs):
    input_1 = all_labels \
        .groupBy(all_labels.question_id) \
        .agg(collect_list(struct(all_labels.run_uuid, all_labels.cluster_id)).alias('clusters_1')) \
        .withColumnRenamed('question_id', 'question_id_1')

    input_1.persist()
    input_2 = input_1 \
        .withColumnRenamed('question_id_1', 'question_id_2') \
        .withColumnRenamed('clusters_1', 'clusters_2')

    ph = triangular_matrix \
        .join(input_1, triangular_matrix.sequential_id_1 == input_1.question_id_1) \
        .join(input_2, triangular_matrix.sequential_id_2 == input_2.question_id_2) \
        .select('question_id_1', 'question_id_2', 'clusters_1', 'clusters_2') \
        .withColumn('similarity', calc_similarity_udf(input_1.clusters_1, input_2.clusters_2, lit(total_runs)))

    input_1.unpersist()
    triangular_matrix.unpersist()

    return ph


def calc_similarity(tuples_1, tuples_2, total_runs):
    return len(set(tuples_1).intersection(set(tuples_2))) / total_runs


calc_similarity_udf = udf(calc_similarity, FloatType())
