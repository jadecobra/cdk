import boto3
import os

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

table = boto3.resource('dynamodb').Table(os.environ.get('DYNAMODB_TABLE_NAME'))

def add_count(path):
    return table.update_item(
        Key={'path': path},
        UpdateExpression='ADD hits :incr',
        ExpressionAttributeValues={':incr': 1},
        ReturnValues='UPDATED_NEW',
    )

def get_path(event):
    return event.get('rawPath')

def handler(event, context):
    add_count(get_path(event))
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f'Hello! You have hit {get_path(event)}\n'
    }