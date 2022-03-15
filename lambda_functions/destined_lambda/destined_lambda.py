def handler(event, context):
    print('Event Received ', event)
    for record in event['Records']:
        message = record['Sns']['Message']
        if message == 'please fail':
            print('received failure flag, throwing error')
            raise Exception('test')
    return {
        'source': 'cdkpatterns.the-destined-lambda',
        'action': 'message',
        'message': 'hello world'
    }