#!/bin/bash
set -e

DOCKER_IMAGE_NAME=$1
AWS_REGION=$2
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO_URI="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$DOCKER_IMAGE_NAME"

docker build -t $DOCKER_IMAGE_NAME -f deployment/docker/Dockerfile.batch .
docker tag "$DOCKER_IMAGE_NAME:latest" "$REPO_URI:latest"
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$REPO_URI"
docker push "$REPO_URI:latest"