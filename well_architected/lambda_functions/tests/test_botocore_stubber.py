import datetime
import boto3

from botocore.stub import Stubber
from datetime import datetime
from unittest import TestCase


def expected_response() -> dict:
    return {
        'Contents': [
            {
                'ETag': '"abc123"',
                'Key': 'test.txt',
                'LastModified': datetime(2016, 1, 20, 22, 9),
                'Owner': {
                    'DisplayName': 'owner', 'ID': 'abc123'
                },
                'Size': 14814,
                'StorageClass': 'STANDARD'
            }
        ],
        'IsTruncated': False,
        'MaxKeys': 1000,
        'Name': 'test-bucket',
        'Prefix': '',
    }

def request() -> dict:
    return {'Bucket': 'test-bucket'}

class TestS3(TestCase):

    def test_list_buckets(self):
        s3 = boto3.client('s3')
        stubber = Stubber(s3)
        stubber.add_response('list_objects', expected_response(), request())
        stubber.activate()

        self.assertEqual(
            s3.list_objects(**request()),
            expected_response()
        )