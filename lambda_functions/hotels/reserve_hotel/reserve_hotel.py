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
    if event['run_type'] == 'failFlightsConfirmation':
        raise Exception('Failed to book the flights')
    booking_id = hash(f'{event["trip_id"]}{event["hotel"]}{event["check_in"]}')
    result = TABLE.put_item(
        Item={
            'booking_id': event['trip_id'],
            'booking_type': f'HOTEL#{booking_id}',
            'type': 'Hotel',
            'trip_id': event['trip_id'],
            'hotel': event['hotel'],
            'id': booking_id,
            'check_in': event['check_in'],
            'check_out': event['check_out'],
            'transaction_status': 'pending',
        }
    )

    print('inserted hotel booking:')
    print(result)

    return {
        'status': 'ok',
        'booking_id': booking_id,
    }
