import json
import boto3
import time
import os
import datetime

eventbridge = boto3.client('events')
# table = boto3.resource('dynamodb').Table(os.environ.get('ERROR_RECORDS'))
# do resources require a connection?

def delimiter():
    print('='*80)

def header(message):
    delimiter()
    print(f'\t{message}')
    delimiter()

def event_bridge_entry(error_type=None, service_url=None):
    print('\t--- EventBridge Response ---');
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


def service_call_failure_after(seconds=1, service_url=None):
    header('\tCalling Webservice, recent errors below threshold');
    time.sleep(seconds)
    print('\t--- Service Call Failure ---');
    errorType = '\t\tservice timeout exception'
    print(errorType)
    print('\t--- EventBridge Response ---');
    return {
        'DetailType': 'httpcall',
        'EventBusName': 'default',
        'Source': 'cdkpatterns.eventbridge.circuitbreaker',
        'Time': datetime.datetime.now(),
        'Detail': json.dumps({
            'status': 'fail',
            'siteUrl': service_url,
            'errorType': errorType
        })
    }

def call_fake_service(serviceURL):

    print('\t--- EventBridge Response ---');
    print(
        # eventbridge.put_events(
        #     Entries=[
        #         {
        #             'DetailType': 'httpcall',
        #             'EventBusName': 'default',
        #             'Source': 'cdkpatterns.eventbridge.circuitbreaker',
        #             'Time': datetime.datetime.now(),
        #             'Detail': json.dumps({
        #                 'status': 'fail',
        #                 'siteUrl': serviceURL,
        #                 'errorType': errorType
        #             })
        #         }
        #     ]
        # )
    )

def circuit_breaker(recentErrors=None, serviceURL=None):
    if len(recentErrors) < 3:
        call_fake_service(serviceURL)
        return send_response(
            500,
            'Something appears to be wrong with this service, please try again later'
        )
    else:
        print('Circuit currently closed, sending back failure response');
        return send_response(
            500,
            'This service has been experiencing issues for a while, we have closed the circuit'
        )

def send_response(status, body):
    return {
        'statusCode': status,
        'headers': {"Content-Type": "text/html"},
        body: body
    }

def handler(event, context):
    serviceURL = 'www.google.com'

    recentErrors = table.query(
        ExpressionAttributeValues={
            ":v1": { "S": serviceURL },
            ":now": { "N": str(time.time()) }
        },
        KeyConditionExpression="SiteUrl = :v1 and ExpirationTime > :now",
        IndexName="UrlIndex",
    )

    print('--- Recent Errors ---');
    print(len(recentErrors));
    print(json.dumps(recentErrors));

    return circuit_breaker(serviceURL=serviceURL, recentErrors=recentErrors)