import math
from ensembles.dao.ensembles_dao import distance_matrix_schema
from utils import general_utils as gu
from pyspark.sql.types import FloatType
from pyspark.sql.functions import udf
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from multiprocessing import Process, Array

triangular_matrix_schema = StructType([StructField("sequential_id_1", IntegerType(), True),
                                       StructField("sequential_id_2", IntegerType(), True),
                                       StructField("question_1", StringType(), True),
                                       StructField("question_2", StringType(), True)])


def build(spark, technique, triangular_matrix, comparator):
    gu.print_screen('Getting distance matrix technique')

    if technique == 'bow' or technique == 'tfidf' or technique == 'w2v':
        return build_distributedly(triangular_matrix, comparator)
    else:
        return build_centrally(spark, triangular_matrix, comparator)


def build_distributedly(triangular_matrix, comparator):
    calculate_similarity = udf(comparator.compare, FloatType())
    distance_matrix = triangular_matrix \
        .withColumn('similarity', calculate_similarity(triangular_matrix.question_1, triangular_matrix.question_2))

    return distance_matrix \
        .where(distance_matrix.similarity > 0) \
        .select('sequential_id_1', 'sequential_id_2', 'similarity')


def build_centrally(spark, triangular_matrix, comparator):
    """
    Temporary method in master to be able to get results in some experiments (serialization issues).
    """
    triangular_matrix_array = triangular_matrix.collect()
    similarity_matrix_array = []
    similarity_matrix_array_shared = Array('f', len(triangular_matrix_array))
    multiprocessing_compare(triangular_matrix_array, similarity_matrix_array_shared, comparator)

    index = 0
    for row in triangular_matrix_array:
        similarity = similarity_matrix_array_shared[index]
        if similarity > 0:
            row_dict = {'sequential_id_1': row.sequential_id_1,
                        'sequential_id_2': row.sequential_id_2,
                        'similarity': similarity_matrix_array_shared[index]}
            similarity_matrix_array.append(Row(**row_dict))
        index += 1

    return spark.createDataFrame(similarity_matrix_array, distance_matrix_schema)


def multiprocessing_compare(triangular_matrix_array, similarity_matrix_arrray, comparator, num_workers=8):
    total = len(triangular_matrix_array)
    matrix_size = math.ceil(total / num_workers)
    index_from = 0
    index_to = matrix_size

    workers = []
    for i in range(num_workers):
        if index_from >= total:
            break

        worker = Process(target=compare_pairs,
                         args=(triangular_matrix_array[index_from:index_to], similarity_matrix_arrray, index_from, comparator))
        worker.start()
        workers.append(worker)

        index_from += matrix_size
        index_to += matrix_size if index_to + matrix_size <= total else total

    # Waits until the workers finish their work
    for worker in workers:
        worker.join()


def compare_pairs(triangular_matrix_array, similarity_matrix_array, index_from, comparator):
    start_index = index_from
    for row in triangular_matrix_array:
        similarity_matrix_array[start_index] = comparator.compare(row.question_1, row.question_2)
        start_index += 1


def get_triangular_matrix(questions_input):
    """
    Gets combinations without repetition. Excludes main diagonal.
    """
    input_1 = questions_input \
        .withColumnRenamed('sequential_id', 'sequential_id_1') \
        .withColumnRenamed('question', 'question_1')

    input_2 = questions_input \
        .withColumnRenamed('sequential_id', 'sequential_id_2') \
        .withColumnRenamed('question', 'question_2')

    return input_1.crossJoin(input_2) \
        .where(input_1.sequential_id_1 < input_2.sequential_id_2)


def get_individual_questions_from_pairs(sample, sample_size):
    """
    Gets a sample of questions with shape [sequential_id, question]

    n = sample_size * 2 # Number of individual questions.
    """
    question_1_sample = sample.selectExpr('sequential_id', 'question_1 as question')
    question_2_sample = sample \
        .withColumn('sequential_id', (sample.sequential_id + sample_size).cast(IntegerType())) \
        .selectExpr('sequential_id', 'question_2 as question')
    return question_1_sample.union(question_2_sample)
