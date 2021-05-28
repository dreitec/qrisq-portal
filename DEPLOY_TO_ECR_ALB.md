# QRisq ECR Deployment

## Install aws cli version 2 and configure
1. Download and install aws cli version 2
https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html

2. Configure aws and Add Access Key ID, Secret Access Key, Region Name and output format [Reference: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html]
```sh
aws configure
```

## Deploy Docker image to ECR
1. Rename .env file as .env.local

2. Rename .env.production as .env

3. Login to ECR
```sh
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 099053078595.dkr.ecr.us-east-1.amazonaws.com
```

4. Build docker image and Push to ECR
```sh
docker build -f Dockerfile.production -t qrisq_api .
docker tag qrisq_api:latest 099053078595.dkr.ecr.us-east-1.amazonaws.com/qrisq_api:latest
docker push 099053078595.dkr.ecr.us-east-1.amazonaws.com/qrisq_api:latest
```