import boto3
import os
import random

''' input example:
{
    trip_id: some_guid,
    depart: london,
    depart_at: some_date,
    arrive: dublin,
    arrive_at: some_date,
    hotel: holiday inn,
    check_in: some_date,
    check_out: some_date,
    rental: volvo,
    rental_from: some_date,
    rental_to: some_date
}
'''

TABLE = boto3.resource('dynamodb').Table(os.environ.get('TABLE_NAME'))

def handler(event, context):
    print(f"request: {event}")
    flight_booking_id = event['ReserveFlightResult']['Payload']['booking_id']
    hotel_booking_id = event['ReserveHotelResult']['Payload']['booking_id']
    payment_id = hash(f'{event["trip_id"]}{hotel_booking_id}{flight_booking_id}')
    result = TABLE.put_item(
        Item={
            'booking_id': event['trip_id'],
            'booking_type': f'PAYMENT#{payment_id}',
            'type': 'Payment',
            'trip_id': event['trip_id'],
            'id': payment_id,
            'amount': '450.00'
            'currency': 'USD',
            'transaction_status': 'confirmed',
        }
    )

    print('payment processed successfully:')
    print(result)

    return {
        'status': 'ok',
        'payment_id': payment_id,
    }