from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
import sys
from pydantic import BaseModel

from libs.aws_utils.secrets import get_secret_value
from libs.aws_utils.glue import get_job_start_time
from libs.ticketmaster.venues.client import VenueRequests
from libs.utils import write_list_model_newline_json, get_logger


logger = get_logger()


class ProcessConf(BaseModel):
    """Attributes for process"""

    output_data_path: str
    secret_name: str
    job_name: str
    job_run_id: str


def process(conf: ProcessConf) -> None:
    """Downloads venue data from ticketmaster API and writes to json in S3"""
    creds = get_secret_value(conf.secret_name)

    venue_client = VenueRequests(api_key=creds["consumer_key"])

    venues, _ = venue_client.get_all_venues()
    logger.info(f"Loaded {len(venues)} venue records from Ticketmaster")
    job_run_date = get_job_start_time(
        job_name=conf.job_name, job_run_id=conf.job_run_id
    )
    full_output_path = f"{conf.output_data_path}/process_date={job_run_date}/data.json"
    write_list_model_newline_json(file_path=full_output_path, model_list=venues)
    logger.info(f"Venues data written to {full_output_path}")


if __name__ == "__main__":
    # Intialize session and context objects
    sc = SparkContext.getOrCreate()

    glue_context = GlueContext(sc)
    job = Job(glue_context)

    args = getResolvedOptions(sys.argv, ["JOB_NAME", "output_data_path", "secret_name"])
    conf = ProcessConf(
        output_data_path=args["output_data_path"],
        secret_name=args["secret_name"],
        job_name=args["JOB_NAME"],
        job_run_id=args["JOB_RUN_ID"],
    )

    job.init(job_name=args["JOB_NAME"])

    process(conf)

    job.commit()
