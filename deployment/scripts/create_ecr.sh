#!/bin/bash
set -e

# Ver se o repositorio de imagens no ecr ja existe
REPO_NAME=$1
AWS_REGION=$2

# Verifica se o repositório já existe
if aws ecr describe-repositories --repository-names "$REPO_NAME" --region "$AWS_REGION" > /dev/null 2>&1; then
    echo "Repositório já existe."
else
    # Se não, cria o repositorio
    echo "Criando repositório..."
    aws ecr create-repository --repository-name "$REPO_NAME" --region "$AWS_REGION"
fi