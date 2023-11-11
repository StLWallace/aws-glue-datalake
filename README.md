# aws-glue-datalake
Using Pyspark with AWS Glue to build an analytics data lake using the Ticketmaster Discovery API. The process is orchestrated by a Glue workflow, and then the final data can be queried using Athena.

# Glue workflow steps
1. Download raw data from Ticketmaster APIs
    a. events-raw job: gets event data
    b. venues-raw job: gets venue data
    c. both jobs run in parallel and write to json files partitioned by the process_date
2. Clean raw data
    a. events-processed job: performs transforms on events data to make it more consumable
    b. venues-processed job: same as above for venues
    c. each job starts after successful completion of its "raw" predecessor
    d. jobs write to parquet, partitioned by process_date
3. Crawl processed data
    a. Glue crawler refreshes schema and partitions for ticketmaster.events and ticketmaster.venues tables
    b. crawler is triggered after both "processed" jobs complete successfully


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

## Ticketmaster API Key
To create a personal (free) Ticketmaster Discovery API key, follow the steps on https://developer.ticketmaster.com/products-and-docs/apis/getting-started/ to create a key. After you've created your key, save the value to load into AWS secrets manager later.

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

4. (First time only) Set secret value for API key
After creating your Ticketmaster API key and running `terraform apply`, set the value of `ticketmaster-api-key-{env}` as:
```
{
  "consumer_key": "consumer key value",
  "consumer_secret": "consumer secret value"
}
replacing the values with your real ones.
```

If the apply succeeded and you loaded the secret, your jobs should be ready to run.
