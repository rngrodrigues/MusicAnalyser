# core/spark_session.py
from pyspark.sql import SparkSession

def get_spark():

    spark = (
        SparkSession.builder
        .appName("Top10Musicas")
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .getOrCreate()
    )
    return spark
