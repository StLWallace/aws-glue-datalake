"""Reads in raw venue data, cleans it, and writes it to s3 as parquet"""

from pyspark.context import SparkContext
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.column import Column
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
import sys
from pydantic import BaseModel

from libs.aws_utils.glue import get_job_start_time
from libs.utils import get_logger


logger = get_logger()


class ProcessConf(BaseModel):
    """Attributes for process"""

    output_data_path: str
    raw_data_path: str
    job_name: str
    job_run_id: str


def format_address() -> Column:
    """Reshapes the address field and other attributes into a more logical struct"""
    line1 = F.col("address.line1").alias("street")
    city = F.col("city.name").alias("city")
    state = F.col("state")
    country = F.col("country")
    postal_code = F.col("postal_code")

    col_exp = F.struct(line1, city, state, postal_code, country).alias("address")

    return col_exp


def extract_markets() -> Column:
    """Market only has 'id' key, so this flattens the list"""
    col_exp = F.expr("transform(markets, m -> m.id)").alias("markets")
    return col_exp


def process(conf: ProcessConf, spark: SparkSession) -> None:
    """Reads data json, cleans, and writes to parquet"""
    df = spark.read.json(path=conf.raw_data_path)
    job_start_time = get_job_start_time(conf.job_name, conf.job_run_id)
    df_processed = df.select(
        "name",
        "type",
        "id",
        "locale",
        format_address(),
        "timezone",
        "location",
        extract_markets(),
        "test",
        "process_date",
    )
    df_processed.write.partitionBy("process_date").mode("overwrite").parquet(
        conf.output_data_path
    )
    logger.info(f"Processed venues data written to {conf.output_data_path}")


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
