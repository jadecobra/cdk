import boto3
import os
import random

TABLE = boto3.resource('dynamodb').Table(os.environ.get('TABLE_NAME'))

def handler(event, context):
    print(f"request: {event}")
    if random.random() < 0.4:
        raise Exception('Internal Server Error')
    booking_id = event['ReserveFlightResult']['Payload']['booking_id']
    result = TABLE.delete_item(
        Key={
            'booking_id': { event.get('trip_id') },
            'booking_type': { f'FLIGHT#{event.get(booking_id)}'}
        }
    )

    print('deleted flight booking:')
    print(result)
    return { 'status': "ok" }