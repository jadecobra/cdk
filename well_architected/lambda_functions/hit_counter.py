import boto3
import os

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

table = boto3.resource('dynamodb').Table(os.environ['HITS_TABLE_NAME'])

def handler(event, context):
    return table.update_item(
        Key={'path': event.get('path')},
        UpdateExpression='ADD hits :incr',
        ExpressionAttributeValues={':incr': 1}
    )
