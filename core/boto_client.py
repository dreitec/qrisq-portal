import os
import logging
import datetime
import uuid

from django.conf import settings

import boto3
from botocore.exceptions import ClientError, ParamValidationError

logger = logging.getLogger(__name__)


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
        logger.warn(filename + ' WKT file not downloaded; ClientError: ' + err.response['Error']['Message'])
        raise err
    except ParamValidationError as err:
        logger.warn(filename + ' WKT file not downloaded; ParamValidationError: Invalid bucket name')
        raise err
    else:
        logger.info(filename + " WKT file downloaded")


def upload_file(filename):
    try:
        s3 = __s3_client()
        bucket = settings.AWS_WKT_BUCKET
        s3.upload_file(filename, bucket)
    except ClientError as err:
        logger.warn(filename + ' WKT file not uploaded; ClientError: ' + err.response['Error']['Message'])
        raise err
    else:
        logger.warn(filename + " WKT file uploaded")
    pass


def __sqs_client():
    return boto3.client(
        'sqs',
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_SQS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SQS_SECRET_ACCESS_KEY
    )


def __generate_unique_message_deduplicationid(user_id):
    time_now    = datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    uuid4 = str(uuid.uuid4())
    return f"{user_id}-{time_now}-{uuid4}"


def send_message_to_sqs_queue(client_id, address, message_body=(
        'This is a test message to ensure messages are being added to the SQS Queue for a registered client.'
    )):

    sqs_client = __sqs_client()
    try:
        message_deduplicationid = __generate_unique_message_deduplicationid(client_id)

        logger.info("Sending Message to SQS queue.")
        response = sqs_client.send_message(
            QueueUrl=settings.SQS_QUEUE_URL,
            DelaySeconds=0,
            MessageAttributes={
                'UserID': {
                    'DataType': 'String',
                    'StringValue': client_id
                },
                'Address': {
                    'DataType': 'String',
                    'StringValue': address.get('displayText', "")
                },
                'Latitude': {
                    'DataType': 'String',
                    'StringValue': str(address.get('lat', ""))
                },
                'Longitude': {
                    'DataType': 'String',
                    'StringValue': str(address.get('lng', ""))
                }
            },
            MessageBody = message_body,
            MessageDeduplicationId = message_deduplicationid,
            MessageGroupId = 'TestMessageGroupID'
        )
        logger.info('De-Duplication ID:' + message_deduplicationid)
        logger.info('Message ID: ' + response['MessageId'])
        logger.info('Message sent to SQS Queue.')

    except ClientError as err:
        logger.error('Message not sent to SQS queue; ClientError: ' + err.response['Error']['Message'])
        raise err

    except ParamValidationError as err:
        logger.error('Message not sent to SQS queue; ' + str(err))
        raise err
