import boto3
import os

dynamodb = boto3.resource('dynamodb')

def handler(event, context=None):
    return {'statusCode': 200, 'body': 'Hello World'}