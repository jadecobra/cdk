import boto3
import random
import string
import time

table = boto3.resource('dynamodb').Table(os.environ.get('ERROR_TABLE_NAME'))

def generate_random_request_id():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

def handler(event, context):
    print(
        table.put_item(
            Item={
                'RequestID': { generate_random_request_id() },
                'SiteUrl': { event['detail']['siteUrl'] },
                'ErrorType': { event['detail']['errorType'] },
                'ExpirationTime': { time.time() + 60 }
            }
        )
    )