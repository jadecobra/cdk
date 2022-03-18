import boto3
import json
import os

step_functions = boto3.client('stepfunctions')


def response(status=200, body=None):
    return {
        'statusCode': status,
        'message': body
    }
def handler(event, context):
    try:
        step_functions.start_execution(
            stateMachineArn=os.environ.get('statemachine_arn'),
            input=json.dumps({
                "trip_id": event['queryStringParameters']['tripID'],
                "depart": "London",
                "depart_at": "2021-07-10T06:00:00.000Z",
                "arrive": "Dublin",
                "arrive_at": "2021-07-12T08:00:00.000Z",
                "hotel": "holiday inn",
                "check_in": "2021-07-10T12:00:00.000Z",
                "check_out": "2021-07-12T14:00:00.000Z",
                "rental": "Volvo",
                "rental_from": "2021-07-10T00:00:00.000Z",
                "rental_to": "2021-07-12T00:00:00.000Z",
                "run_type": event['queryStringParameters']['runType']
            })
        )
    except Exception as error:
        return response(
            status=500,
            body=f'Failed to process order because: {error}'
        )
    else:
        return response(
            body='The holiday booking system is processing your order'
        )