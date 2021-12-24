import os
# os.system('npm install -g npm@8.3.0')
from aws_cdk.core import App
from api_gateway import LambdaAPIGateway
from waf import WebApplicationFirewall
from lambda_function import LambdaFunction

app = App()
WebApplicationFirewall(
    app, 'WebApplicationFirewall',
    target_arn=LambdaAPIGateway(
        app, 'LambdaAPIGateway',
        lambda_function=LambdaFunction(
            app, 'LambdaFunction',
        ).lambda_function
    ).resource_arn
)
app.synth()