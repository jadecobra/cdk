import os
# os.system('npm install -g npm@8.3.0')
from aws_cdk.core import App
from api_gateway import LambdaAPIGateway
from web_application_firewall import WebApplicationFirewall
from lambda_function import LambdaFunction

class WellArchitected(App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        WebApplicationFirewall(
            self, 'WebApplicationFirewall',
            target_arn=self.create_lambda_api_gateway(
                self.create_lambda_function()
            )
        )

    def create_lambda_function(self):
        return LambdaFunction(
            self, 'LambdaFunction',
            function_name='hello',
        ).lambda_function

    def create_lambda_api_gateway(self, lambda_function):
        return LambdaAPIGateway(
            self, 'LambdaAPIGateway',
            lambda_function=lambda_function
        ).resource_arn


WellArchitected().synth()