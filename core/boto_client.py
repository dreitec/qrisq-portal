import os
import logging

from django.conf import settings

import boto3
from botocore.exceptions import ClientError

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)


def __s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY,
        region_name=settings.AWS_REGION
    )


def download_file(filename):
    try:
        s3 = __s3_client()
        bucket = settings.AWS_WKT_BUCKET
        with open(filename, 'wb') as f:
            s3.download_fileobj(bucket, filename, f)
    except ClientError as err:
        os.remove(filename)
        print(filename + ' WKT file not downloaded; ClientError: ' + err.response['Error']['Message'])
        raise err
        # logger.info(filename + ' WKT file not downloaded; ClientError: ' + err.response['Error']['Message'])
    else:
        # logger.info(filename + " WKT file downloaded")
        print(filename + " WKT file downloaded")


def upload_file(filename):
    try:
        s3 = __s3_client()
        bucket = settings.AWS_WKT_BUCKET
        s3.upload_file(filename, bucket)
    except ClientError as err:
        print(filename + ' WKT file not uploaded; ClientError: ' + err.response['Error']['Message'])
        raise err
        # logger.info(filename + ' WKT file not downloaded; ClientError: ' + err.response['Error']['Message'])
    else:
        # logger.info(filename + " WKT file downloaded")
        print(filename + " WKT file uploaded")
    pass