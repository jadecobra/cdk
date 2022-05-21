import circuit_breaker
import random
import json

def unreliable():
    if random.random() < 0.6:
        return 'Success'
    return 'Failed'

def fallback():
    return 'Fallback'

def handler(event=None, context=None):
    message = circuit_breaker.CircuitBreaker(
        request=unreliable,
        fallback=fallback,
        failure_threshold=3,
        success_threshold=2,
        timeout=10000
    ).fire()

    return {
        'statusCode': 200,
        'body': json.dumps({
            message: message
        })
    }
