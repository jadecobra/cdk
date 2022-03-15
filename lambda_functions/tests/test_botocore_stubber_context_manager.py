import datetime
import boto3

from botocore.stub import Stubber
from datetime import datetime
from unittest import TestCase

s3 = boto3.client('s3')

def expected_response():
    return {
        'Owner': {
            'ID': 'foo',
            'DisplayName': 'bar'
        },
        'Buckets': [{
            'CreationDate': datetime(2016, 1, 20, 22, 9),
            'Name': 'baz'
        }]
    }


class TestS3(TestCase):

    def test_list_buckets(self):
        with Stubber(s3) as stubber:
            stubber.add_response('list_buckets', expected_response(), {})
            self.assertEqual(s3.list_buckets(), expected_response())