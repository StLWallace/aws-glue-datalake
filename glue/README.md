# Glue Scripts and Configs
This directory contains python libraries and configs for Pyspark jobs.


## jobs
This directory should only contain "main" files for each Glue job. Each file in this directory will be uploaded automatically to the /jobs/ location in the Glue scripts S3 bucket.

## libs
This directory contains additional libraries that can be imported in the jobs. This directory will be zipped and loaded to s3. The zipped location is reference in the `--extra-py-files` Glue default arg.

## tests
Unit tests for the jobs and libraries. To run:
`pytest tests/`
