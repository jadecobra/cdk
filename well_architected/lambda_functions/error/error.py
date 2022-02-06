import boto3
import random
import string
import time

table = boto3.resource('dynamodb').Table(os.environ.get('ERROR_TABLE_NAME'))

def handler(event, context):
    return table.put_item(
        Item={
            'RequestID': { ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10)) },
            'SiteUrl': { event['detail']['siteUrl'] },
            'ErrorType': { event['detail']['errorType'] },
            'ExpirationTime': { time.time() + 60 }
        }
    )