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

def handler(flavor):
    print(f"Requested Pizza : {flavor}")
    contains_pineapple = False
    if flavor == 'pineapple' or flavor == 'hawaiian':
        contains_pineapple = True
    return { 'containsPineapple': contains_pineapple}