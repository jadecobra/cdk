import unittest
import lambda_functions.webservice.webservice as webservice
import datetime
import json


class TestWebservice(unittest.TestCase):

    def test_failing(self):
        self.assertEqual(6, 6)

    @unittest.expectedFailure
    def test_event_bridge_entry(self):
        self.assertEqual(
            webservice.create_event_bridge_entry(
                error_type='ErrorType',
                service_url='ServiceURL',
            ),
            {
                'DetailType': 'httpcall',
                'EventBusName': 'default',
                'Source': 'cdkpatterns.eventbridge.circuitbreaker',
                'Time': datetime.datetime.now(),
                'Detail': json.dumps({
                    'status': 'fail',
                    'siteUrl': 'ServiceURL',
                    'errorType': 'ErrorType'
                })
            }
        )

    def test_create_service_timeout_exception_after_raises(self):
        with self.assertRaises(webservice.ServiceTimeoutException):
            webservice.create_service_timeout_exception_after(0)

    def test_circuit_breaker_when_errors_are_less_than_3(self):
        self.assertEqual(
            webservice.circuit_breaker(
                recent_errors=2,
                service_url='service-url'
            ),
            {

            }
        )

    def test_circuit_breaker_on_3_or_more_errors(self):
        self.assertEqual(
            webservice.circuit_breaker(
                recent_errors=3,
                service_url='service-url'
            ),
            {

            }
        )
        self.assertEqual(
            webservice.circuit_breaker(
                recent_errors=4,
                service_url='service-url'
            ),
            {

            }
        )

    # def test_call_fake_service_returns_none(self):
    #     self.assertEqual(webservice.call_fake_service('test'), '')

    def test_table_query(self):
        return {
    'Items': [
        {
            'string': "'string'|123|Binary(b'bytes')|True|None|set(['string'])|set([123])|set([Binary(b'bytes')])|[]|{}"
        },
    ],
    'Count': 123,
    'ScannedCount': 123,
    'LastEvaluatedKey': {
        'string': "'string'|123|Binary(b'bytes')|True|None|set(['string'])|set([123])|set([Binary(b'bytes')])|[]|{}"
    },
    'ConsumedCapacity': {
        'TableName': 'string',
        'CapacityUnits': 123.0,
        'ReadCapacityUnits': 123.0,
        'WriteCapacityUnits': 123.0,
        'Table': {
            'ReadCapacityUnits': 123.0,
            'WriteCapacityUnits': 123.0,
            'CapacityUnits': 123.0
        },
        'LocalSecondaryIndexes': {
            'string': {
                'ReadCapacityUnits': 123.0,
                'WriteCapacityUnits': 123.0,
                'CapacityUnits': 123.0
            }
        },
        'GlobalSecondaryIndexes': {
            'string': {
                'ReadCapacityUnits': 123.0,
                'WriteCapacityUnits': 123.0,
                'CapacityUnits': 123.0
            }
        }
    }
}