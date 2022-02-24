import boto3
import datetime
import os

sqs = boto3.client('sqs')

def send_response(status=200, body=None):
    return {
        'statusCode': status,
        'body': body,
        'headers': {
            "Content-Type": "text/html"
        },
    }

def handler(event, context):
    print('request: ', event)

    try:
        response = sqs.send_message(
            DelaySeconds=10,
            MesageAttributes={
                'QueueUrl': os.environ.get('queueURL'),
                'MessageBody': f'Hello from {event["path"]}',
                'MessageDeduplicationId': {
                    'DataType': 'String',
                    'StringValue': f'{event["path"]}{datetime.datetime.now()}'
                }
            }
        )
    except Exception as error:
        send_response(500, error)
    else:
        send_response('You have added a message to the queue! Message ID is ' + response['MessageId'])