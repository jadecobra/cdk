import json
import boto3
import time
import os
import datetime

# EVENT_BRIDGE = boto3.client('events')
# DYNAMODB_TABLE = boto3.resource('dynamodb').Table(os.environ.get('DYNAMODB_TABLE_NAME'))
# do resources require a connection?


class ServiceTimeoutException(Exception):pass


def delimiter():
    print('='*80)

def header(message):
    delimiter()
    print(f'\t{message}')
    delimiter()

def create_event_bridge_entry(error_type=None, service_url=None):
    return {
        'DetailType': 'httpcall',
        'EventBusName': 'default',
        'Source': 'cdkpatterns.eventbridge.circuitbreaker',
        'Time': datetime.datetime.now(),
        'Detail': json.dumps({
            'status': 'fail',
            'siteUrl': service_url,
            'errorType': error_type
        })
    }

def create_service_timeout_exception_after(seconds):
    time.sleep(seconds)
    raise ServiceTimeoutException

def write_event_bridge_event(service_url):
    EVENT_BRIDGE.put_events(
        Entries=[
            create_service_timeout_exception_after(0)
        ]
    )

def call_fake_service(serviceURL):
    pass

def circuit_breaker(recent_errors=None, service_url=None):
    if len(recent_errors) < 3:
        try:
            create_service_timeout_exception_after(0)
        except  ServiceTimeoutException:
            return send_response(
                500,
                'ServiceTimeoutException'
            )
    else:
        return send_response(
            500,
            'ServiceTimeOutError'
        )

def send_response(status, body):
    return {
        'statusCode': status,
        'headers': {"Content-Type": "text/html"},
        body: body
    }

def handler(event, context):
    serviceURL = 'www.google.com'

    recentErrors = DYNAMODB_TABLE.query(
        ExpressionAttributeValues={
            ":v1": { "S": serviceURL },
            ":now": { "N": str(time.time()) }
        },
        KeyConditionExpression="SiteUrl = :v1 and ExpirationTime > :now",
        IndexName="UrlIndex",
    )

    print('--- Recent Errors ---')
    print(len(recentErrors))
    print(json.dumps(recentErrors))

    return circuit_breaker(service_url=serviceURL, recent_errors=recentErrors)