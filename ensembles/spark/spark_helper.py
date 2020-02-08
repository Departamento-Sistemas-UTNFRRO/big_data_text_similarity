from pyspark.sql import SparkSession


def create_spark_session():
    return SparkSession.builder \
        .master("local[12]") \
        .config("spark.ui.port", "4050") \
        .config("spark.driver.memory", "12g") \
        .appName("big_data_text_similarity") \
        .enableHiveSupport() \
        .getOrCreate()
