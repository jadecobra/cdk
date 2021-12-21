import boto3
import os

dynamodb = boto3.resource('dynamodb')

def send_response(status=None, body=None):
    return {
        'statusCode': status,
        'body': body,
        'headers': {
            'Content-Type': 'text/html',
        },
    }

def handler(event, context):
    dynamodb.update_item(
        TableName=os.environ['HITS_TABLE_NAME'],
        UpdateExpression: 'ADD hits :incr',
        ExpressionAttributeValues: { ':incr': { N: '1'}},
        Key={
            "path": {
                'S': event['path']
            }
        }
    )
    print(f'inserted counter for {event["path"]}')
    return send_response(status='200', body='You have connected with the HitCounter!')