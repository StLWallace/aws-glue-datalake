"""Reads in raw event data, cleans it, and writes it to s3 as parquet"""

from pyspark.context import SparkContext
from pyspark.sql import SparkSession, DataFrame, functions as F
from pyspark.sql.column import Column
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
import sys
from pydantic import BaseModel
from typing import Literal

from libs.aws_utils.glue import get_job_start_time


class ProcessConf(BaseModel):
    """Attributes for process"""

    output_data_path: str
    raw_data_path: str
    job_name: str
    job_run_id: str


def extract_start_date() -> Column:
    """Extracts start date from a Date struct field"""
    col_exp = F.col("dates.start.local_date").alias("start_date")
    return col_exp


def extract_sales(attr: Literal["start_date_time", "end_date_time"]) -> Column:
    """Extracts nested attributes from sales struct
    Args:
        attr - name of lowest level attribute to extract
    """
    new_col_name = f"sales_{attr}"
    col_exp = F.col(f"sales.public.{attr}").alias(new_col_name)
    return col_exp


def process(conf: ProcessConf, spark: SparkSession) -> None:
    """Reads data json, cleans, and writes to parquet"""
    events_raw = spark.read.json(path=conf.raw_data_path)
    job_start_time = get_job_start_time(conf.job_name, conf.job_run_id)
    events_processed = events_raw.select(
        "classifications",
        extract_start_date(),
        "images",
        "locale",
        "name",
        "promoter",
        extract_sales("start_date_time"),
        extract_sales("end_date_time"),
        "test",
        "type",
        "url",
        "process_date",
    )
    events_processed.write.partitionBy("process_date").mode("overwrite").parquet(
        conf.output_data_path
    )


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
