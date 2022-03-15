import boto3
import os

table = boto3.resource('dynamodb').Table(os.environ.get('tableName'))

def handler(event, context):
    for record in event['Records']:
        payload = record['body']

        print('received message: ', payload)
        table.put_item(
            Item={
                'id': record['messageAttributes']['MessageDeduplicationId']['stringValue'],
                'message': payload
            }
        )