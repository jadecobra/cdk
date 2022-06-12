from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
from random import randint
from urllib.request import urlopen

import aws_xray_sdk.core
aws_xray_sdk.core.patch_all()

def handler(event, context):
    if randint(0, 9) < 4:
        raise Exception("Random error")
    with urlopen("http://www.google.com") as response:
        return response.read()
