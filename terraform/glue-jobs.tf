# This process creates S3 objects for Glue code and the defines the Glue jobs

# Upload all Python files in the glue/jobs/ directory to S3
locals {
  scripts_path = "s3://${aws_s3_bucket.glue_scripts.id}/jobs"
}
resource "aws_s3_object" "glue_job_scripts" {
  for_each = fileset("../glue/jobs", "*.py")
  bucket   = aws_s3_bucket.glue_scripts.id
  key      = "jobs/"
  source   = "../glue/jobs/${each.value}"

  # The filemd5() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the md5() function and the file() function:
  # etag = "${md5(file("path/to/file"))}"
  etag = filemd5("../glue/jobs/${each.value}")
}


resource "aws_glue_job" "test_job" {
  name = "test-job-${var.environment}"
  role_arn = aws_iam_role.glue.arn

  glue_version = "4.0"
  command {
    name = "glueetl"
    script_location = "${local.scripts_path}/test_job.py"
  }
}
