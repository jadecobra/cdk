import boto3
import os
import random

TABLE = boto3.resource('dynamodb').Table(os.environ.get('TABLE_NAME'))

def handler(event, context):
    print(f"request: {event}")
    if event['run_type'] == 'failFlightsConfirmation':
        raise Exception('Failed to book the flights')
    booking_id = event['ReserveFlightResult']['Payload']['booking_id']
    result = TABLE.add_item(
        Key={
            'booking_id': { event.get('trip_id') },
            'booking_type': { f'FLIGHT#{event.get(booking_id)}'}
        },
        UpdateExpression='set transaction_status = :booked',
        ExpressionAttributeValues={
            ':booked': {'S': 'confirmed'}
        }
    )

    print('confirmed flight booking:')
    print(result)

    return {
        'status': 'ok',
        'booking_id': booking_id,
    }