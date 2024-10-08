#!/bin/bash
set -e

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_NAME="$ACCOUNT_ID-prediction-eml"
AWS_REGION=$1

# Verifica se o bucket existe
if aws s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null; then
    echo "O bucket '$BUCKET_NAME' já existe."
else
    # Se o bucket não existir, cria o bucket
    aws s3api create-bucket --bucket "$BUCKET_NAME" --region us-east-1
    echo "Bucket '$BUCKET_NAME' criado com sucesso."
fi

terraform -chdir="deployment/infrastructure/terraform-lambda" init -backend-config="bucket=$BUCKET_NAME" -backend-config="region=$AWS_REGION"
terraform -chdir="deployment/infrastructure/terraform-lambda" apply -auto-approve