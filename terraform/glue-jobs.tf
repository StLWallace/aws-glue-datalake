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
    "--spark-event-logs-path"            = "s3://${aws_s3_bucket.data_lake.id}/spark-ui-logs/"
  }
  execution_class = "STANDARD"
}
