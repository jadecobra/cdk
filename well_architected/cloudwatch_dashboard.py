import cloudwatch

from aws_cdk.core import Stack, Construct, Duration
from aws_cdk.aws_lambda import Function
from aws_cdk.aws_dynamodb import Table
from aws_cdk.aws_cloudwatch_actions import SnsAction
from aws_cdk.aws_sns import Topic
from aws_cdk.aws_cloudwatch import (
    Alarm, Dashboard, Metric, TreatMissingData, Unit
)
from api_gateway_cloudwatch import ApiGatewayCloudWatch

class CloudWatchDashboard(Stack):

    def __init__(
        self, scope: Construct, id: str,
        lambda_function: Function = None,
        lambda_function_cloudwatch_widgets=None,
        dynamodb_table: Table = None,
        dynamodb_cloudwatch_widgets: list = None,
        api_gateway_cloudwatch_widgets: tuple = None,
        api_id: str = None,
        error_topic: Topic = None,
        widgets=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.api_id = api_id
        # self.error_topic = error_topic
        # self.dynamodb_table = dynamodb_table
        self.dynamodb_cloudwatch_widgets = dynamodb_cloudwatch_widgets
        # self.lambda_function = lambda_function
        self.lambda_function_cloudwatch_widgets = lambda_function_cloudwatch_widgets
        # self.api_gateway_cloudwatch = ApiGatewayCloudWatch(
        #     self, 'ApiGatewayCloudWatch',
        #     api_id=self.api_id,
        #     error_topic=self.error_topic,
        # )
        # self.api_gateway_cloudwatch_widgets = self.api_gateway_cloudwatch.api_gateway_cloudwatch_widgets
        self.api_gateway_cloudwatch_widgets = api_gateway_cloudwatch_widgets
        self.create_cloudwatch_dashboard(
            self.api_gateway_cloudwatch_widgets,
            self.lambda_function_cloudwatch_widgets,
            self.dynamodb_cloudwatch_widgets,
        )

    def create_cloudwatch_dashboard(self, *widgets):
        self.dashboard = Dashboard(self, "CloudWatchDashBoard")
        for widget in widgets:
            self.dashboard.add_widgets(*widget)