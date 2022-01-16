from aws_cdk.core import App
from rest_api import LambdaRestAPIGateway
from web_application_firewall import WebApplicationFirewall
from lambda_function import LambdaFunction

from cloudwatch_dashboard import CloudWatchDashboard
from dynamodb_table import DynamoDBTable
from http_api import LambdaHttpApiGateway
from sns_topic import SnsTopic
from xray_tracer.xray_tracer import TheXrayTracerStack
from xray_tracer.sqs_flow import SqsFlow
from xray_tracer.sns_flow import SnsFlow
from xray_tracer.dynamodb_flow import DynamoDBFlow
from xray_tracer.http_flow import HttpFlow

class WellArchitected(App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_topic = SnsTopic(self, 'SnsTopic').topic
        self.dynamodb_table = self.create_dynamodb_table(self.error_topic)
        self.lambda_function = self.create_lambda_function(
            error_topic=self.error_topic,
            environment_variables={
                'HITS_TABLE_NAME': self.dynamodb_table.dynamodb_table.table_name
            }
        )
        self.dynamodb_table.dynamodb_table.grant_read_write_data(self.lambda_function.lambda_function)
        self.create_rest_api()
        self.create_http_api()

        xray_tracer = TheXrayTracerStack(self, 'XRayTracer')
        HttpFlow(self, 'HttpFlow', sns_topic=xray_tracer.sns_topic)
        DynamoDBFlow(self, 'DynamoDBFlow', sns_topic=xray_tracer.sns_topic)
        SnsFlow(self, 'SnsFlow', sns_topic=xray_tracer.sns_topic)
        SqsFlow(self, 'SqsFlow', sns_topic=xray_tracer.sns_topic)

    def create_http_api(self):
        self.http_api = LambdaHttpApiGateway(
            self, 'LambdaHttpApiGateway',
            lambda_function=self.lambda_function.lambda_function,
            error_topic=self.error_topic,
        )

    def create_rest_api(self):
        self.rest_api = LambdaRestAPIGateway(
            self, 'LambdaRestAPIGateway',
            lambda_function=self.lambda_function.lambda_function,
            error_topic=self.error_topic,
        )

        self.create_web_application_firewall(
            id='WebApplicationFirewall',
            target_arn=self.rest_api.resource_arn,
        )

    def create_dynamodb_table(self, error_topic):
        return DynamoDBTable(
            self, 'DynamoDBTable',
            error_topic=error_topic
        )

    def create_lambda_function(self, environment_variables=None, error_topic=None):
        return LambdaFunction(
            self, 'LambdaFunction',
            function_name='hello',
            environment_variables=environment_variables,
            error_topic=error_topic
        )

    def create_web_application_firewall(self, id=None, target_arn=None):
        return WebApplicationFirewall(self, id, target_arn=target_arn)

WellArchitected().synth()