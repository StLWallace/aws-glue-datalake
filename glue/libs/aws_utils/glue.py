import boto3
from datetime import datetime as dt


def get_job_start_time(job_name: str, job_run_id: str, glue_client=None) -> str:
    """Gets start time from an AWS Glue job object
    Args:
        job_name - name of job
        job_run_id - run ID for job
        glue_client - a boto3 glue client

    Returns:
        a string of the start time for the job
    """
    if glue_client is None:
        glue_client = boto3.client("glue")

    response = glue_client.get_job_run(
        JobName=job_name, RunId=job_run_id, PredecessorsIncluded=False
    )
    start_time = response["JobRun"]["StartedOn"].strftime("%Y-%m-%d")

    return start_time
