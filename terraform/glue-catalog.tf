resource "aws_glue_catalog_database" "ticketmaster" {
  name = "ticketmaster-${var.environment}"
}


resource "aws_glue_crawler" "ticketmaster" {
  database_name = aws_glue_catalog_database.ticketmaster.name
  name          = "ticketmaster_${var.environment}"
  role          = aws_iam_role.glue.arn

  s3_target {
    path = "s3://${aws_s3_bucket.data_lake.bucket}/processed/ticketmaster"
  }

  configuration = jsonencode(
    {
      Grouping = {
        TableLevelConfiguration = 3
      }
      Version = 1
    }
  )
}
