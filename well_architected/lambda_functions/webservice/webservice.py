import json
import boto3
import time
import os
import datetime

eventbridge = boto3.client('events')
dynamo = boto3.client('dynamodb')

def call_fake_service(serviceURL):
    # In here assume we made an http request to google and it was down,
    # 10 sec hard coded delay for simulation

    print('--- Calling Webservice, recent errors below threshold ---');
    time.sleep(10)
    print('--- Service Call Failure ---');
    errorType = 'service timeout exception'
    print(errorType)

    print('--- EventBridge Response ---');
    print(
        eventbridge.put_events(
            Entries=[
                {
                    'DetailType': 'httpcall',
                    'EventBusName': 'default',
                    'Source': 'cdkpatterns.eventbridge.circuitbreaker',
                    'Time': datetime.datetime.now(),
                    'Detail': json.dumps({
                        'status': 'fail',
                        'siteUrl': serviceURL,
                        'errorType': errorType
                    })
                }
            ]
        )
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
    serviceURL = 'www.google.com';

    recentErrors = dynamo.query(
        ExpressionAttributeValues={
            ":v1": { "S": serviceURL },
            ":now": { "N": str(time.time()) }
        },
        KeyConditionExpression="SiteUrl = :v1 and ExpirationTime > :now",
        IndexName="UrlIndex",
        TableName=os.environ.get('ERROR_RECORDS'),
    )

    print('--- Recent Errors ---');
    print(len(recentErrors));
    print(json.dumps(recentErrors));

    return circuit_breaker(serviceURL=serviceURL, recentErrors=recentErrors)