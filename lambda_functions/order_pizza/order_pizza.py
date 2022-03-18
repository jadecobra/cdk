'''
SAMPLE REQUESTS

Failing Request
{
    "flavor": "pineapple"
}

Successful Request
{
    "flavor": "pepperoni"
}

'''

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

def handler(flavor):
    print(f"Requested Pizza : {flavor}")
    contains_pineapple = False
    if flavor == 'pineapple' or flavor == 'hawaiian':
        contains_pineapple = True
    return { 'containsPineapple': contains_pineapple}