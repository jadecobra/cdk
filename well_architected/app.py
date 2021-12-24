import os
# os.system('npm install -g npm@8.3.0')
from aws_cdk.core import App
from api_gateway import LambdaAPIGateway
from waf import Waf

app = App()
api_stack = LambdaAPIGateway(app, 'LambdaAPIGateway')
Waf(app, 'WebApplicationFirewall', target_arn=api_stack.resource_arn)
app.synth()