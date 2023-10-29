# Create IAM role and policies for Glue
data "aws_iam_policy_document" "glue_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "glue" {
  name               = "AWSGlueServiceRoleDefault"
  assume_role_policy = data.aws_iam_policy_document.glue_assume_role.json
}

# Attach AWS predefined policy
resource "aws_iam_role_policy_attachment" "glue_service_role" {
  role       = aws_iam_role.glue.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# S3 Access
data "aws_iam_policy_document" "glue_s3" {
  statement {
    actions = [
      "s3:*",
    ]
    resources = [
      aws_s3_bucket.data_lake.arn,
      "${aws_s3_bucket.data_lake.arn}/*",
      aws_s3_bucket.glue_scripts.arn,
      "${aws_s3_bucket.glue_scripts.arn}/*",
    ]
  }
}

resource "aws_iam_policy" "glue_s3" {
  name   = "glue-s3-${var.environment}"
  policy = data.aws_iam_policy_document.glue_s3.json
}

resource "aws_iam_role_policy_attachment" "glue_s3" {
  role       = aws_iam_role.glue.name
  policy_arn = aws_iam_policy.glue_s3.arn
}

# Secret access
data "aws_iam_policy_document" "glue_secrets" {
  statement {
    actions = [
      "secretsmanager:DescribeSecret",
      "secretsmanager:GetSecretValue",
      "secretsmanager:ListSecrets"
    ]
    resources = [aws_secretsmanager_secret.ticketmaster_api_key.arn]
  }
}

resource "aws_iam_policy" "glue_secrets" {
  name   = "glue-secrets-${var.environment}"
  policy = data.aws_iam_policy_document.glue_secrets.json
}

resource "aws_iam_role_policy_attachment" "glue_secrets" {
  role       = aws_iam_role.glue.name
  policy_arn = aws_iam_policy.glue_secrets.arn
}
