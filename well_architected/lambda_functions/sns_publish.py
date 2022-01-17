import boto3
import os

sns = boto3.client('sns', region_name='us-east-1')

def handler(event, context):
    return sns.publish(
        TopicArn=os.environ.get('TOPIC_ARN'),
        Message='Simulated Message',
    )