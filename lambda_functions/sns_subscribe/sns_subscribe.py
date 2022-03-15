from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

def handler(event, context):
    return event['Records'][0]['Sns']['Message']