#!/bin/bash
set -e

# Ver se o repositorio de imagens no ecr ja existe
REPO_NAME=$1
REGION=$2

# Verifica se o repositório já existe
if aws ecr describe-repositories --repository-names "$REPO_NAME" --region "$REGION" > /dev/null 2>&1; then
    echo "Repositório já existe."
else
    # Se não, cria o repositorio
    echo "Criando repositório..."
    aws ecr create-repository --repository-name "$REPO_NAME" --region "$REGION"
fi

# # Se sim, recupera a URI do repo
# ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
# REPO_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME"

# # Builda a imagem
# IMAGE_NAME="minha-imagem"
# docker build -t "$IMAGE_NAME" .

# # Faz do docker tag da imagem
# docker tag "$IMAGE_NAME:latest" "$REPO_URI:latest"

# # Faz o login no repositorio
# aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "$REPO_URI"

# # Faz o push da imagem
# docker push "$REPO_URI:latest"
