import os

from aws_cdk.core import App
from rest_api import LambdaRestAPIGateway
from web_application_firewall import WebApplicationFirewall
from lambda_function import LambdaFunction

from cloudwatch_dashboard import CloudWatchDashboard
from dynamodb_table import DynamoDBTable
from http_api import LambdaHttpApiGateway
from sns_topic import SnsTopic

class WellArchitected(App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_topic = SnsTopic(self, 'SnsTopic').topic
        self.dynamodb_table = self.create_dynamodb_table(self.error_topic)
        self.lambda_function = self.create_lambda_function(
            environment_variables={
                'HITS_TABLE_NAME': self.dynamodb_table.dynamodb_table.table_name
            }
        )
        self.http_api = self.create_http_api_gateway(self.lambda_function).http_api
        self.rest_api = self.create_rest_api_gateway(self.lambda_function)

        self.dynamodb_table.dynamodb_table.grant_read_write_data(self.lambda_function)
        self.create_web_application_firewall(
            id='WebApplicationFirewall',
            target_arn=self.rest_api.resource_arn,
        )

        CloudWatchDashboard(
            self, 'HttpApiCloudWatchDashboard',
            lambda_function=self.lambda_function,
            dynamodb_table=self.dynamodb_table.dynamodb_table,
            dynamodb_cloudwatch_widgets=self.dynamodb_table.dynamodb_cloudwatch_widgets,
            api_id=self.http_api.api_id,
            error_topic=self.error_topic,
        )

        CloudWatchDashboard(
            self, 'RestApiCloudWatchDashboard',
            lambda_function=self.lambda_function,
            dynamodb_table=self.dynamodb_table.dynamodb_table,
            dynamodb_cloudwatch_widgets=self.dynamodb_table.dynamodb_cloudwatch_widgets,
            api_id=self.rest_api.rest_api.rest_api_id,
            error_topic=self.error_topic,
        )

        # TODO
        # put alarms with individual components
        # put metrics with individual components
        # add alarms to dashboard from individual components
        # add big fan topic pattern

    def create_dynamodb_table(self, error_topic):
        return DynamoDBTable(
            self, 'DynamoDBTable',
            error_topic=error_topic
        )

    def create_http_api_gateway(self, lambda_function):
        return LambdaHttpApiGateway(
            self, 'LambdaHttpApiGateway',
            lambda_function=lambda_function,
        )

    def create_lambda_function(self, environment_variables):
        return LambdaFunction(
            self, 'LambdaFunction',
            function_name='hello',
            environment_variables=environment_variables,
        ).lambda_function

    def create_rest_api_gateway(self, lambda_function):
        return LambdaRestAPIGateway(
            self, 'LambdaRestAPIGateway',
            lambda_function=lambda_function
        )

    def create_cloudwatch_dashboard(self, id=None, lambda_function=None, dynamodb_table=None, api=None):
        return CloudWatchDashboard(
            self, 'CloudWatchDashboard',
            lambda_function=lambda_function,
            dynamodb_table=dynamodb_table,
            api=api,
        )

    def create_web_application_firewall(self, id=None, target_arn=None):
        return WebApplicationFirewall(
            self, id,
            target_arn=target_arn
        )

WellArchitected().synth()