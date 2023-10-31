# This process creates S3 objects for Glue code and the defines the Glue jobs

# Upload all Python files in the glue/jobs/ directory to S3
locals {
  scripts_path = "s3://${aws_s3_bucket.glue_scripts.id}/jobs"
}
resource "aws_s3_object" "glue_job_scripts" {
  for_each = fileset("../glue/jobs", "*.py")
  bucket   = aws_s3_bucket.glue_scripts.id
  key      = "jobs/${each.value}"
  source   = "../glue/jobs/${each.value}"

  etag = filemd5("../glue/jobs/${each.value}")
}

# Zip and upload glue libraries to S3
# To make the structure of the zip archive match the import layout in the code, we need to have a /libs/ folder inside the zip
# To do this, we zip the /glue/ directory and then exclude everything except the /libs/ folder
data "archive_file" "glue_libs" {
  source_dir  = "../glue"
  output_path = "libs.zip"
  type        = "zip"
  excludes = setunion(fileset("../glue", "jobs/**"), fileset("../glue", "tests/**")
  )
}

resource "aws_s3_object" "glue_libs" {
  bucket = aws_s3_bucket.glue_scripts.id
  key    = "libs.zip"
  source = data.archive_file.glue_libs.output_path
  etag   = filemd5(data.archive_file.glue_libs.output_path)
}


## Jobs
# This is just a "hello world" job
resource "aws_glue_job" "test_job" {
  name              = "test-job-${var.environment}"
  role_arn          = aws_iam_role.glue.arn
  number_of_workers = 2
  worker_type       = "G.1X"

  glue_version = "4.0"
  command {
    name            = "glueetl"
    script_location = "${local.scripts_path}/test_job.py"
  }
  default_arguments = {
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-job-insights"              = "true"
    "--enable-spark-ui"                  = "true"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://${aws_s3_bucket.data_lake.id}/spark-ui-logs/test-job/"
  }
  execution_class = "STANDARD"
}

/* Venues raw data job
default_arguments:
  output_data_path - location where the downloaded data will be written (in S3)
  secret_name - name of AWS SecretsManager secret that contains the Ticketmaster API creds
*/
resource "aws_glue_job" "venues_raw" {
  name              = "venues-raw-${var.environment}"
  role_arn          = aws_iam_role.glue.arn
  number_of_workers = 2
  worker_type       = "G.1X"
  execution_property {
    max_concurrent_runs = 2
  }

  glue_version = "4.0"
  command {
    name            = "glueetl"
    script_location = "${local.scripts_path}/venues_raw.py"
  }
  default_arguments = {
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-job-insights"              = "true"
    "--enable-spark-ui"                  = "true"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://${aws_s3_bucket.data_lake.id}/spark-ui-logs/venues-raw/"
    "--output_data_path"                 = "s3://${aws_s3_bucket.data_lake.id}/raw/ticketmaster/venues"
    "--secret_name"                      = aws_secretsmanager_secret.ticketmaster_api_key.id
    "--additional-python-modules"        = "smart_open,pydantic"
    "--extra-py-files"                   = "s3://${aws_s3_bucket.glue_scripts.id}/libs.zip"
  }
  execution_class = "STANDARD"
}

/* Venues processed data job
default_arguments:
  output_data_path - location where the downloaded data will be written (in S3)
  secret_name - name of AWS SecretsManager secret that contains the Ticketmaster API creds
*/
resource "aws_glue_job" "venues_processed" {
  name              = "venues-processed-${var.environment}"
  role_arn          = aws_iam_role.glue.arn
  number_of_workers = 2
  worker_type       = "G.1X"
  execution_property {
    max_concurrent_runs = 2
  }

  glue_version = "4.0"
  command {
    name            = "glueetl"
    script_location = "${local.scripts_path}/venues_processed.py"
  }
  default_arguments = {
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-job-insights"              = "true"
    "--enable-spark-ui"                  = "true"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://${aws_s3_bucket.data_lake.id}/spark-ui-logs/venues-processed/"
    "--raw_data_path"                    = "s3://${aws_s3_bucket.data_lake.id}/raw/ticketmaster/venues"
    "--output_data_path"                 = "s3://${aws_s3_bucket.data_lake.id}/processed/ticketmaster/venues"
    "--additional-python-modules"        = "smart_open,pydantic"
    "--extra-py-files"                   = "s3://${aws_s3_bucket.glue_scripts.id}/libs.zip"
  }
  execution_class = "STANDARD"
}


/* Events raw data job
default_arguments:
  output_data_path - location where the downloaded data will be written (in S3)
  secret_name - name of AWS SecretsManager secret that contains the Ticketmaster API creds
*/
resource "aws_glue_job" "events_raw" {
  name              = "events-raw-${var.environment}"
  role_arn          = aws_iam_role.glue.arn
  number_of_workers = 2
  worker_type       = "G.1X"
  execution_property {
    max_concurrent_runs = 2
  }

  glue_version = "4.0"
  command {
    name            = "glueetl"
    script_location = "${local.scripts_path}/events_raw.py"
  }
  default_arguments = {
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-job-insights"              = "true"
    "--enable-spark-ui"                  = "true"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://${aws_s3_bucket.data_lake.id}/spark-ui-logs/events-raw/"
    "--output_data_path"                 = "s3://${aws_s3_bucket.data_lake.id}/raw/ticketmaster/events"
    "--secret_name"                      = aws_secretsmanager_secret.ticketmaster_api_key.id
    "--additional-python-modules"        = "smart_open,pydantic"
    "--extra-py-files"                   = "s3://${aws_s3_bucket.glue_scripts.id}/libs.zip"
  }
  execution_class = "STANDARD"
}


/* Events processed data job
default_arguments:
  output_data_path - location where the downloaded data will be written (in S3)
  secret_name - name of AWS SecretsManager secret that contains the Ticketmaster API creds
*/
resource "aws_glue_job" "events_processed" {
  name              = "events-processed-${var.environment}"
  role_arn          = aws_iam_role.glue.arn
  number_of_workers = 2
  worker_type       = "G.1X"
  execution_property {
    max_concurrent_runs = 2
  }

  glue_version = "4.0"
  command {
    name            = "glueetl"
    script_location = "${local.scripts_path}/events_processed.py"
  }
  default_arguments = {
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-job-insights"              = "true"
    "--enable-spark-ui"                  = "true"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://${aws_s3_bucket.data_lake.id}/spark-ui-logs/events-processed/"
    "--raw_data_path"                    = "s3://${aws_s3_bucket.data_lake.id}/raw/ticketmaster/events"
    "--output_data_path"                 = "s3://${aws_s3_bucket.data_lake.id}/processed/ticketmaster/events"
    "--additional-python-modules"        = "smart_open,pydantic"
    "--extra-py-files"                   = "s3://${aws_s3_bucket.glue_scripts.id}/libs.zip"
  }
  execution_class = "STANDARD"
}
