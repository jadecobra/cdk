import boto3
import datetime

event_bridge = boto3.client('events')

def events():
    return {
        'Entries': [
            {
                'Source': 'custom.myATMapp',
                'EventBusName': 'default',
                'DetailType': 'transaction',
                'Time': datetime.datetime.now(datetime.timezone.utc),
                'Detail': {
                    'action': 'withdrawal',
                    'location': 'MA-BOS-01',
                    'amount': 300,
                    'result': 'approved',
                    'transactionId': '123456',
                    'cardPresent': True,
                    'partnerBank': 'Example Bank',
                    'remainingFunds': 722.34
                }
            },
            {
                'Source': 'custom.myATMapp',
                'EventBusName': 'default',
                'DetailType': 'transaction',
                'Time': datetime.datetime.now(datetime.timezone.utc),
                'Detail': {
                    'action': 'withdrawal',
                    'location': 'NY-NYC-001',
                    'amount': 20,
                    'result': 'approved',
                    'transactionId': '123457',
                    'cardPresent': True,
                    'partnerBank': 'Example Bank',
                    'remainingFunds': 212.52
                }
            },
            {
                'Source': 'custom.myATMapp',
                'EventBusName': 'default',
                'DetailType': 'transaction',
                'Time': datetime.datetime.now(datetime.timezone.utc),
                'Detail': {
                    'action': 'withdrawal',
                    'location': 'NY-NYC-002',
                    'amount': 60,
                    'result': 'denied',
                    'transactionId': '123458',
                    'cardPresent': True,
                    'remainingFunds': 5.77
                }
            }
        ]
    }

def handler(event, context):
    print('--- Response ---')
    print(event_bridge.put_events(events()))

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': 'You have sent the events to EventBridge!'
    }
