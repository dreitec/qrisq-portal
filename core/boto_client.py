import logging

from django.conf import settings

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)


def __s3_client():
    try:
        client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION
        )
    except (ClientError, NoCredentialsError) as error:
        print(error.response['Error']['Message'])
    else:
        return client


def download_file(filename):
    try:
        s3 = __s3_client()
        bucket = 'qrisq-webapp-data-v2'
        with open(filename, 'wb') as f:
            s3.download_fileobj(bucket, filename, f)
    except ClientError as err:
        print("Client Error while downloading files")
        # logger.info(filename + ' WKT file not downloaded; ClientError: ' + err.response['Error']['Message'])
    else:
        # logger.info(filename + " WKT file downloaded")
        print(filename + " WKT file downloaded")
