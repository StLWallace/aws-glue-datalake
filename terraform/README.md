<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | 2.4.0 |
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.23.1 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_athena_workgroup.default](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/athena_workgroup) | resource |
| [aws_glue_catalog_database.ticketmaster](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_catalog_database) | resource |
| [aws_glue_crawler.ticketmaster](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_crawler) | resource |
| [aws_glue_job.events_processed](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.events_raw](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.test_job](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.venues_processed](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.venues_raw](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_trigger.crawler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_trigger) | resource |
| [aws_glue_trigger.events_processed](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_trigger) | resource |
| [aws_glue_trigger.start](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_trigger) | resource |
| [aws_glue_trigger.venues_processed](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_trigger) | resource |
| [aws_glue_workflow.ticketmaster](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_workflow) | resource |
| [aws_iam_policy.glue_s3](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_policy.glue_secrets](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.glue](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.glue_s3](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.glue_secrets](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.glue_service_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_s3_bucket.data_lake](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket.glue_scripts](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | resource |
| [aws_s3_object.glue_job_scripts](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.glue_libs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_secretsmanager_secret.ticketmaster_api_key](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/secretsmanager_secret) | resource |
| [archive_file.glue_libs](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.glue_assume_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.glue_s3](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.glue_secrets](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_environment"></a> [environment](#input\_environment) | Name of deployment environment | `string` | n/a | yes |
| <a name="input_region"></a> [region](#input\_region) | Default AWS region | `string` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->
