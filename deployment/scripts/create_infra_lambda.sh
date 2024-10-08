#!/bin/bash
set -e

AWS_REGION=$1

terraform -chdir="deployment/infrastructure/terraform-lambda" init
terraform -chdir="deployment/infrastructure/terraform-lambda" apply -auto-approve