import boto3
import time
import os
import csv
import datetime
import json

EVENT_BRIDGE = boto3.client('events')
S3 = boto3.resource('s3')

def download_s3_object(filename=None, bucket_name=None, object_key=None):
    return S3.Object(
        os.environ.get(bucket_name),
        os.environ.get(object_key)
    ).download_file(filename)

def get_detail(headers=None, row=None):
    return json.dumps({
        'status': 'extracted',
        'headers': ','.join(headers),
        'data': ','.join(row)
    })

def main(filename):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = next(reader)
        for row in reader:
            print(', '.join(row))
            response = EVENT_BRIDGE.put_events(
                Entries=[
                    {
                        'DetailType': 's3RecordExtraction',
                        'EventBusName': 'default',
                        'Source': 'cdkpatterns.the-eventbridge-etl',
                        'Time': datetime.now(),
                        'Detail': get_detail(
                            headers=headers,
                            row=row
                        )
                    },
                ]
            )
    exit(0)

if __name__ == '__main__':
    filename='/tmp/data.tsv'
    download_s3_object(
        bucket_name='S3_BUCKET_NAME',
        object_key='S3_OBJECT_KEY',
        filename=filename,
    )
    main(filename)