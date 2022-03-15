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
    booking_id = hash(f'{event["trip_id"]}{event["depart"]}{event["arrive"]}')
    result = TABLE.put_item(
        Item={
            'booking_id': event['trip_id'],
            'booking_type': f'FLIGHT#{booking_id}',
            'type': 'Flight',
            'trip_id': event['trip_id'],
            'id': booking_id,
            'depart': event['depart'],
            'depart_at': event['depart_at'],
            'arrive': event['arrive'],
            'arrive_at': event['arrive_at'],
            'transaction_status': 'pending',
        }
    )

    print('inserted flight booking:')
    print(result)

    return {
        'status': 'ok',
        'booking_id': booking_id,
    }