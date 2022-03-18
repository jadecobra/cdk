import boto3
import os
import random

TABLE = boto3.resource('dynamodb').Table(os.environ.get('TABLE_NAME'))

def handler(event, context):
    print(f"request: {event}")
    if event['run_type'] == 'failHotelConfirmation':
        raise Exception('Failed to book the hotel')
    booking_id = event['ReserveHotelResult']['Payload']['booking_id']
    result = TABLE.update_item(
        Key={
            'booking_id': { event.get('trip_id') },
            'booking_type': { f'HOTEL#{event.get(booking_id)}'}
        },
        UpdateExpression='set transaction_status = :booked',
        ExpressionAttributeValues={
            ':booked': {'S': 'confirmed'}
        }
    )

    print('updated hotel booking booking:')
    print(result)

    return {
        'status': 'ok',
        'booking_id': booking_id,
    }