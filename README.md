# aws-glue-datalake
Using Pyspark with AWS Glue to build an analytics data lake. The process is orchestrated by a Glue workflow, and then the final data is exposed using a Crawler.


# Deployment
The process of creating the supporting AWS resources and uploading code artifacts for jobs is managed through Terraform. Before running this, create an S3 state bucket and a DynamoDB table for state locking manually or in a different repo. The DynamoDB table must have PK = "LockID" of type string.

Create a file called `terraform/backend-demo.tfvars` with the following lines:
```
bucket         = "{name of your state bucket}"
key            = "{s3 key for your Terraform state file}"
region         = "{AWS region for the bucket}"
dynamodb_table = "{name of your state lock DDB table}"
```
