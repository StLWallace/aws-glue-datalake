"""Reads in raw venue data, cleans it, and writes it to s3 as parquet"""

from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
import sys
from pydantic import BaseModel

from libs.aws_utils.glue import get_job_start_time


class ProcessConf(BaseModel):
    """Attributes for process"""

    output_data_path: str
    raw_data_path: str
    job_name: str
    job_run_id: str


def process(conf: ProcessConf, spark: SparkSession) -> None:
    """Reads data json, cleans, and writes to parquet"""
    df = spark.read.json(path=conf.raw_data_path)
    job_start_time = get_job_start_time(conf.job_name, conf.job_run_id)

    df.write.partitionBy("process_date").parquet(conf.output_data_path)


if __name__ == "__main__":
    # Intialize session and context objects
    sc = SparkContext.getOrCreate()
    spark = SparkSession(sc)

    glue_context = GlueContext(sc)
    job = Job(glue_context)

    args = getResolvedOptions(
        sys.argv, ["JOB_NAME", "output_data_path", "raw_data_path"]
    )
    conf = ProcessConf(
        output_data_path=args["output_data_path"],
        raw_data_path=args["raw_data_path"],
        job_name=args["JOB_NAME"],
        job_run_id=args["JOB_RUN_ID"],
    )

    job.init(job_name=args["JOB_NAME"])

    process(conf, spark)

    job.commit()
