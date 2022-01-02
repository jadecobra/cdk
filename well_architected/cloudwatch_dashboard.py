import cloudwatch

from aws_cdk.core import Stack, Construct, Duration
from aws_cdk.aws_lambda import Function
from aws_cdk.aws_dynamodb import Table
from aws_cdk.aws_cloudwatch_actions import SnsAction
from aws_cdk.aws_sns import Topic
from aws_cdk.aws_cloudwatch import (
    Alarm, Dashboard, Metric, TreatMissingData, Unit
)


class CloudWatchDashboard(Stack):

    def __init__(
        self, scope: Construct, id: str,
        lambda_function: Function = None,
        lambda_function_cloudwatch_widgets=None,
        dynamodb_table: Table = None,
        dynamodb_cloudwatch_widgets: list = None,
        api_id: str = None,
        error_topic: Topic = None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.api_id = api_id
        self.error_topic = error_topic
        self.dynamodb_table = dynamodb_table
        self.dynamodb_cloudwatch_widgets = dynamodb_cloudwatch_widgets
        self.lambda_function = lambda_function
        self.lambda_function_cloudwatch_widgets = lambda_function_cloudwatch_widgets
        self.create_metrics()
        self.create_cloudwatch_alarms()
        self.create_cloudwatch_dashboard()

    def create_api_gateway_metrics(self):
        self.api_gateway_4xx_error_percentage = cloudwatch.create_cloudwatch_math_expression(
            expression="m1/m2*100",
            label="% API Gateway 4xx Errors",
            using_metrics={
                "m1": self.add_api_gateway_metric(
                    metric_name='4XXError',
                    label='4XX Errors',
                ),
                "m2": self.add_api_gateway_metric(
                    metric_name='Count',
                    label='# Requests',
                ),
            },
        )

    def add_api_gateway_metric(self, metric_name: str = None, label: str = None,
        period=Duration.seconds(900), statistic: str = 'sum'):
        return Metric(
            metric_name=metric_name,
            namespace="AWS/ApiGateway",
            dimensions_map={"ApiId": self.api_id},
            unit=Unit.COUNT,
            label=label,
            statistic=statistic,
            period=period,
        )

    def create_api_gateway_alarms(self):
        # 4xx are user errors so a large volume indicates a problem
        self.create_cloudwatch_alarm(
            id="API Gateway 4XX Errors > 1%",
            metric=self.api_gateway_4xx_error_percentage
        )

        # 5xx are internal server errors so we want 0 of these
        self.create_cloudwatch_alarm(
            id="API Gateway 5XX Errors > 0",
            metric=self.add_api_gateway_metric(
                metric_name="5XXError",
                label="5XX Errors",
                statistic="p99"
            ),
            threshold=0,
        )

        self.create_cloudwatch_alarm(
            id="API p99 latency alarm >= 1s",
            metric=self.add_api_gateway_metric(
                metric_name="Latency",
                label="API GW Latency",
                statistic="p99",
            ),
            threshold=1000,
        )

    def create_cloudwatch_alarms(self):
        self.create_api_gateway_alarms()

    def create_metrics(self):
        self.create_api_gateway_metrics()

    def create_cloudwatch_dashboard(self):
        self.dashboard = Dashboard(self, "CloudWatchDashBoard")
        self.dashboard.add_widgets(
            cloudwatch.create_cloudwatch_widget(
                title="Requests",
                stacked=False,
                left=[
                    self.add_api_gateway_metric(
                        metric_name="Count",
                        label="# Requests",
                    )
                ]
            ),
            cloudwatch.create_cloudwatch_widget(
                title="API GW Latency",
                left=[
                    self.add_api_gateway_metric(
                        metric_name="Latency",
                        label=label,
                        statistic=statistic,
                    ) for label, statistic in (
                        ("API Latency p50", "p50"),
                        ("API Latency p90", "p90"),
                        ("API Latency p99", "p99"),
                    )
                ]
            ),
            cloudwatch.create_cloudwatch_widget(
                title="API GW Errors",
                left=[
                    self.add_api_gateway_metric(
                        metric_name=metric_name,
                        label=label,
                    ) for metric_name, label in (
                        ("4XXError", "4XX Errors"),
                        ("5XXError", "5XX Errors"),
                    )
                ]
            ),
            *self.lambda_function_cloudwatch_widgets,
            *self.dynamodb_cloudwatch_widgets,
        )


    def five_minutes(self):
        return Duration.minutes(5)

    def create_cloudwatch_alarm(self, id=None, metric=None, threshold=1):
        return Alarm(
            self,
            id=id,
            metric=metric,
            threshold=threshold,
            evaluation_periods=6,
            datapoints_to_alarm=1,
            treat_missing_data=TreatMissingData.NOT_BREACHING,
        ).add_alarm_action(
            SnsAction(self.error_topic)
        )