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

        TheXrayTracerStack(self, 'XRayTracer')

        # xray_tracer = TheXrayTracerStack(app, "the-xray-tracer")
        # http_flow = TheHttpFlowStack(app, 'the-http-flow-stack', sns_topic_arn=xray_tracer.sns_topic_arn)
        # dynamo_flow = TheDynamoFlowStack(app, 'the-dynamo-flow-stack', sns_topic_arn=xray_tracer.sns_topic_arn)
        # sns_flow = TheSnsFlowStack(app, 'the-sns-flow-stack', sns_topic_arn=xray_tracer.sns_topic_arn)
        # sqs_flow = TheSqsFlowStack(app, 'the-sqs-flow-stack', sns_topic_arn=xray_tracer.sns_topic_arn)

        # http_flow.add_dependency(xray_tracer)
        # dynamo_flow.add_dependency(xray_tracer)
        # sns_flow.add_dependency(xray_tracer)
        # sqs_flow.add_dependency(xray_tracer)

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