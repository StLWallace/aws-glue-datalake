from pyspark.context import SparkContext
from pyspark.sql import SparkSession, DataFrame
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
import sys


def load_source_data(spark: SparkSession, path: str) -> DataFrame:
    """Reads a csv into a Pyspark dataframe
    Args:
        spark - a spark session
        path - path to the file/s to read into the dataframe
    """
    df = spark.read.option("header", True).option("delimiter", "\t").csv(path=path)

    return df


if __name__ == "__main__":
    # Intialize session and context objects
    sc = SparkContext.getOrCreate()
    spark = SparkSession(sc)

    glue_context = GlueContext(sc)
    job = Job(glue_context)
    args = getResolvedOptions(sys.argv, ["JOB_NAME", "source_data_path"])

    df = load_source_data(spark, path=args["source_data_path"])

    print(f"Columns: {df.columns}")
    print(f"Count: {df.count()}")
