resource "aws_s3_bucket" "data_lake" {
  bucket = "data-lake-${var.environment}-${local.project_id}"

  tags = {
    Name        = "data-lake-${var.environment}"
    Environment = var.environment
  }
}


resource "aws_s3_bucket" "glue_scripts" {
  bucket = "glue-scripts-${var.environment}-${local.project_id}"

  tags = {
    Name        = "glue-scripts-${var.environment}"
    Environment = var.environment
  }
}
