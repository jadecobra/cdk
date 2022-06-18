import boto3
import os

TABLE = boto3.resource(
    'dynamodb'
).Table(
    os.environ.get('DYNAMODB_TABLE_NAME')
)

def handler(event, context):
    for record in event['Records']:
        payload = record['body']

        print('received message: ', payload)
        TABLE.put_item(
            Item={
                'id': record['messageAttributes']['MessageDeduplicationId']['stringValue'],
                'message': payload
            }
        )