# aws-glue-datalake
Using Pyspark with AWS Glue to build an analytics data lake. The process is orchestrated by a Glue workflow, and then the final data is exposed using a Crawler.


# Deployment
The process of creating the supporting AWS resources and uploading code artifacts for jobs is managed through Terraform.

## Pre-setup
Before running this, create an S3 state bucket and a DynamoDB table for state locking manually or in a different repo. The DynamoDB table must have PK = "LockID" of type string.

Create a file called `terraform/backend-demo.tfvars` with the following lines:
```
bucket         = "{name of your state bucket}"
key            = "{s3 key for your Terraform state file}"
region         = "{AWS region for the bucket}"
dynamodb_table = "{name of your state lock DDB table}"
```

## Terraform Steps
Before running, ensure that you have valid AWS credentials in your terminal and a role that allows you to deploy all the resources contained.

1. Initialize
Only run this when you first setup:
`./terraform/scripts/init.sh`

2. Plan
Re-run anytime your configuration changes (including scripts):
`./terraform/scripts/plan.sh`

3. Apply
If the changes outlined in your plan look good, apply them:
`./terraform/scripts/apply.sh`

If the apply succeeded, your jobs should be ready to run.
