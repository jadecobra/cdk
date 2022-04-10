def handler(event, context):
    print('request: ', event)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'level': 'Silver'
    }