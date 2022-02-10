from rest_api import LambdaRestAPIGateway
from web_application_firewall import WebApplicationFirewall
from lambda_function import LambdaFunctionStack
from lambda_layer import LambdaLayer
from dynamodb_table import DynamoDBTableStack
from http_api import LambdaHttpApiGateway
from sns_topic import SnsTopic
from xray_tracer.sns_rest_api import SnsRestApi
from xray_tracer.sqs_flow import SqsFlow
from xray_tracer.sns_flow import SnsFlow
from xray_tracer.dynamodb_flow import DynamoDBFlow
from xray_tracer.http_flow import HttpFlow

import aws_cdk.core as cdk
import event_bridge_circuit_breaker
import aws_cdk.aws_dynamodb as aws_dynamodb

class WellArchitected(cdk.App):

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

        self.xray_sns_topic = SnsTopic(self, 'XRayTracerSnsFanOutTopic', display_name='The XRay Tracer Fan Out Topic').topic
        SnsRestApi(self, 'SnsRestApi', sns_topic=self.xray_sns_topic)
        HttpFlow(self, 'HttpFlow', sns_topic=self.xray_sns_topic)
        DynamoDBFlow(self, 'DynamoDBFlow', sns_topic=self.xray_sns_topic)
        SnsFlow(self, 'SnsFlow', sns_topic=self.xray_sns_topic)
        SqsFlow(self, 'SqsFlow', sns_topic=self.xray_sns_topic)
        event_bridge_circuit_breaker.EventBridgeCircuitBreaker(self, 'EventBridgeCircuitBreaker')

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
        return DynamoDBTableStack(
            self, 'DynamoDBTable',
            error_topic=error_topic,
            partition_key=aws_dynamodb.Attribute(
                name="path",
                type=aws_dynamodb.AttributeType.STRING,
            )
        )

    def create_lambda_function(self, environment_variables=None, error_topic=None):
        return LambdaFunctionStack(
            self, 'LambdaFunction',
            function_name='hit_counter',
            environment_variables=environment_variables,
            error_topic=error_topic
        )

    def create_web_application_firewall(self, id=None, target_arn=None):
        return WebApplicationFirewall(self, id, target_arn=target_arn)

WellArchitected().synth()