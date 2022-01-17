import boto3
import os

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

sqs = boto3.client('sqs', region_name='us-east-1')

def handler(event, context):
    for record in event['Records']:
        print(f'received message: {event["Records"][record]["body"]}')