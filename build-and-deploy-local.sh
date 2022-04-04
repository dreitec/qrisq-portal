#!/usr/bin/env bash
set -e

AWS_ACCOUNT_NUMBER=$(aws sts get-caller-identity --query Account --output text)
VERSION=$(git rev-parse --short HEAD)
ROLE_TO_ASSUME=arn:aws:iam::${AWS_ACCOUNT_NUMBER}:role/qrisq-code-build-service-role

ROLE_CREDS=$(aws sts assume-role --role-arn ${ROLE_TO_ASSUME} --role-session-name local-deployment)
export AWS_ACCESS_KEY_ID=$(echo $ROLE_CREDS | jq -r '.Credentials''.AccessKeyId');\
export AWS_SECRET_ACCESS_KEY=$(echo $ROLE_CREDS | jq -r '.Credentials''.SecretAccessKey');\
export AWS_SESSION_TOKEN=$(echo $ROLE_CREDS | jq -r '.Credentials''.SessionToken');

#echo $AWS_ACCESS_KEY_ID
#echo $AWS_SECRET_ACCESS_KEY
#echo $AWS_SESSION_TOKEN
echo "Prepare to deploy $VERSION..."

AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN} ./build-and-deploy.sh ${VERSION}