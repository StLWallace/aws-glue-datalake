#! /bin/bash
cd terraform
terraform plan -var-file=demo.tfvars -out=demo.tfplan
