import boto3
import os

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

sns = boto3.client('sns', region_name='us-east-1')

def handler(event, context):
    return sns.publish(
        TopicArn=os.environ.get('TOPIC_ARN'),
        Message='Simulated Message',
    )