resource "aws_s3_bucket" "data_lake" {
  bucket = "data-lake-${var.environment}"

  tags = {
    Name        = "data-lake-${var.environment}"
    Environment = var.environment
  }
}


resource "aws_s3_bucket" "glue_scripts" {
  bucket = "glue-scripts-${var.environment}"

  tags = {
    Name        = "glue-scripts-${var.environment}"
    Environment = var.environment
  }
}
