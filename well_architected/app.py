import os

from aws_cdk.core import App
from rest_api import LambdaRestAPIGateway
from web_application_firewall import WebApplicationFirewall
from lambda_function import LambdaFunction

from cloudwatch_dashboard import CloudWatchDashboard
from dynamodb_table import DynamoDBTable
from http_api import LambdaHTTPAPIGateway

class WellArchitected(App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dynamodb_table=self.create_dynamodb_table()
        self.lambda_function = self.create_lambda_function(
            environment_variables={
                'HITS_TABLE_NAME': self.dynamodb_table.table_name
            }
        )
        self.create_web_application_firewall(
            self.create_lambda_api_gateway(self.lambda_function)
        )
        self.create_cloudwatch_dashboard(
            dynamodb_table=self.dynamodb_table,
            lambda_function=self.lambda_function,
            http_api=self.create_http_api_gateway(self.lambda_function).http_api,
        )

    def create_dynamodb_table(self):
        return DynamoDBTable(
            self, 'DynamoDBTable',
        ).dynamodb_table

    def create_http_api_gateway(self, lambda_function):
        return LambdaHTTPAPIGateway(
            self, 'LambdaHTTPAPIGateway',
            lambda_function=lambda_function,
        )

    def create_lambda_function(self, environment_variables):
        return LambdaFunction(
            self, 'LambdaFunction',
            function_name='hello',
            environment_variables=environment_variables,
        ).lambda_function

    def create_lambda_api_gateway(self, lambda_function):
        return LambdaRestAPIGateway(
            self, 'LambdaRestAPIGateway',
            lambda_function=lambda_function
        ).resource_arn

    def create_cloudwatch_dashboard(self, lambda_function=None, dynamodb_table=None, http_api=None):
        return CloudWatchDashboard(
            self, 'CloudWatchDashboard',
            lambda_function=lambda_function,
            dynamodb_table=dynamodb_table,
            http_api=http_api,
        )

    def create_web_application_firewall(self, target_arn):
        return WebApplicationFirewall(
            self, 'WebApplicationFirewall',
            target_arn=target_arn
        )

WellArchitected().synth()