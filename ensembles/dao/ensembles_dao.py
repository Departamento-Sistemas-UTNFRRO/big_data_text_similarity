from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType
from utils import general_utils as gu
import utils.io_utils as io
import csv

PARTITION_NUMBER = 72  # 72 = 6 cores, 12 threads.

sample_schema = StructType([StructField("sequential_id", IntegerType(), True),
                            StructField("pair_id", IntegerType(), True),
                            StructField("question_1", StringType(), True),
                            StructField("question_2", StringType(), True),
                            StructField("duplicate_indicator", IntegerType(), True)])

labels_schema = StructType([StructField("run_uuid", StringType(), True),
                            StructField("question_id", IntegerType(), True),
                            StructField("cluster_id", IntegerType(), True)])

distance_matrix_schema = StructType([StructField("sequential_id_1", IntegerType(), True),
                                     StructField("sequential_id_2", IntegerType(), True),
                                     StructField("similarity", FloatType(), True)])

coassociation_matrix_schema = StructType([StructField("question_id_1", IntegerType(), True),
                                          StructField("question_id_2", IntegerType(), True),
                                          StructField("question_1", StringType(), True),
                                          StructField("question_2", StringType(), True),
                                          StructField("similarity", FloatType(), True)])


def get_questions_from_sample(spark, questions_path):
    gu.print_screen('Getting sample from: ' + questions_path)
    return spark \
        .read \
        .csv(questions_path, header=False, schema=sample_schema) \
        .repartition(PARTITION_NUMBER)


def get_clustering_labels(spark, results_path):
    directory = results_path + '/labels'
    gu.print_screen('Getting all clustering labels from: ' + directory)
    return spark \
        .read \
        .csv(directory, header=False, schema=labels_schema) \
        .repartition(PARTITION_NUMBER)


def get_distance_matrix_from_files(spark, path, technique):
    distance_path = path + '/distances/' + technique
    gu.print_screen('Getting data from path=' + distance_path)
    return spark \
        .read \
        .csv(distance_path, header=True, schema=distance_matrix_schema) \
        .repartition(PARTITION_NUMBER)


def get_coassociation_matrix(spark, path):
    coassociation_matrix_path = path + '/coassociation_matrix'
    return spark \
        .read \
        .csv(coassociation_matrix_path, header=True, schema=coassociation_matrix_schema) \
        .repartition(PARTITION_NUMBER)


def write_clustering_labels(cluster_labels, results_path, k, n, run_uuid):
    directory = results_path + '/labels'
    file_dir = directory + '/labels_ID_' + str(run_uuid) + '_size_' + str(n) + '_clusters_' + str(k) + '.csv'

    with open(file_dir, 'w') as csv_file:
        writer = csv.writer(csv_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for label in cluster_labels:
            writer.writerow(label)


def write_distance_matrix_to_file(df, path, technique):
    distance_path = path + '/distances/' + technique
    io.create_directory(distance_path)
    gu.print_screen('Saving distance matrix to:' + distance_path)
    df \
        .repartition(PARTITION_NUMBER) \
        .write \
        .mode('overwrite') \
        .option("header", "true") \
        .csv(distance_path)


def write_individiual_questions(df, path):
    individual_questions_path = path + '/input'
    io.create_directory(individual_questions_path)
    gu.print_screen('Saving individual questions to:' + individual_questions_path)
    df \
        .repartition(PARTITION_NUMBER) \
        .write \
        .mode('overwrite') \
        .option("header", "true") \
        .csv(individual_questions_path)


def write_coassociation_matrix(df, path):
    coassociation_matrix_path = path + '/coassociation_matrix'
    io.create_directory(coassociation_matrix_path)
    gu.print_screen('Saving co-association matrix to:' + coassociation_matrix_path)
    df \
        .repartition(PARTITION_NUMBER) \
        .write \
        .mode('overwrite') \
        .option("header", "true") \
        .csv(coassociation_matrix_path)
