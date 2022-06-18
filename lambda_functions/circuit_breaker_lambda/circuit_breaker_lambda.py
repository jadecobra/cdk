import boto3
import datetime
import os
import random
import json

ERROR_RECORDS = boto3.resource(
    'dynamodb'
).Table(
    os.environ['DYNAMODB_TABLE_NAME']
)


class CircuitBreaker(object):

    def __init__(
        self,
        request=None, options=None, fallback=None,
        failure_threshold=5, success_threshold=2, timeout=10000
    ):
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout = timeout,
        self.fallback = fallback
        self.state = 'CLOSED'
        self.failure_count = 0
        self.success_count = 0,
        self.next_attempt = datetime.datetime.now()

    @staticmethod
    def get_state():
        return ERROR_RECORDS.get_item(
            Key={
                'id': get_lambda_function_name()
            }
        )['Item']

    def try_fallback(self, fallback):
        print('CircuitBreaker Fallback request')
        try:
            return fallback()
        except Exception:
            raise


    def half(self):
        print('CircuitBreaker state: HALF')
        self.state = 'HALF'

    def set_half_state(self):
        if self.state == 'OPEN':
            if self.next_attempt <= datetime.datetime.now():
                self.half()
            else:
                if self.fallback:
                    return self.try_fallback(self.fallback)
                raise Exception('CircuitBreaker state: OPEN')

    def close(self):
        print('CircuitBreaker state: CLOSED')
        self.success_count = 0
        self.failure_count = 0
        self.state = 'CLOSED'
        return

    def fire(self):
        item_data = self.get_state()['Item']
        self.state = item_data['circuitState']
        self.failure_count = item_data['failureCount']
        self.success_count = item_data['successCount']
        self.next_attempt = item_data['nextAttempt']
        self.set_half_state()

        try:
            response = self.request()
        except Exception:
            return self.fail()
        else:
            return self.success(response)

    def success(self, response):
        if self.state == 'HALF':
            self.success_count += 1
        if self.success_count > self.success_threshold:
            self.close()
        self.failure_count = 0
        self.update_state(
            circuit_state=self.state,
            successes=self.success_count,
            failures=self.failure_count,
        )
        return response

    def failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.open()
        self.update_state(
            circuit_state=self.state,
            successes=self.success_count,
            failures=self.failure_count,
        )

        if self.fallback:
            return self.try_fallback(self.fallback)

    def open(self):
        print('CircuitBreaker state: OPEN')
        self.state = 'OPEN'
        self.next_attempt = datetime.datetime.now() + datetime.timedelta(self.timeout)
        return

    def update_state(self, circuit_state=None, failures=None, successes=None, next_attempt=None):
        return ERROR_RECORDS.update_item(
            Key={
                'id': get_lambda_function_name()
            },
            UpdateExpression='set circuitState=:st, failureCount=:fc, successCount=:sc, nextAttempt=:na, stateTimestamp=:ts',
            ExpressionAttributeValues={
                ':st': circuit_state,
                ':fc': failures,
                ':sc': successes,
                ':na': next_attempt,
                ':ts': datetime.datetime.now()
            },
            ReturnValues='UPDATED_NEW'
        )

def get_lambda_function_name():
    return os.environ['AWS_LAMBDA_FUNCTION_NAME']

def unreliable():
    if random.random() < 0.6:
        return 'Success'
    return 'Failed'

def fallback():
    return 'Fallback'

def handler(event=None, context=None):
    message = CircuitBreaker(
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
