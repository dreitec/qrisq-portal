#!/usr/bin/env bash
set -e

AWS_ACCOUNT_NUMBER=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION="us-east-1"
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_NUMBER}.dkr.ecr.${AWS_REGION}.amazonaws.com

VERSION=$1

UI_IMAGE=${AWS_ACCOUNT_NUMBER}.dkr.ecr.${AWS_REGION}.amazonaws.com/qrisq-ui
API_IMAGE=${AWS_ACCOUNT_NUMBER}.dkr.ecr.${AWS_REGION}.amazonaws.com/qrisq-api

DOCKER_TAG_UI=${UI_IMAGE}:${VERSION}
DOCKER_TAG_API=${API_IMAGE}:${VERSION}

PROCESSING_TEMPLATE=$(cat deployment.yaml | sed "s|{{DOCKER_IMAGE_UI}}|${DOCKER_TAG_UI}|g" | sed "s|{{DOCKER_IMAGE_API}}|${DOCKER_TAG_API}|g")

docker build . -t ${DOCKER_TAG_API}
docker push ${DOCKER_TAG_API}

cd frontend

docker build . -t ${DOCKER_TAG_UI}
docker push ${DOCKER_TAG_UI}

echo "$PROCESSING_TEMPLATE" | kubectl apply -f -