data "aws_caller_identity" "current" {}

locals {
  project_id = data.aws_caller_identity.current.account_id
}
