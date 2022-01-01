import os
from this import d
# os.system('pip install aws_cdk.aws_apigatewayv2_integrations')

from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigatewayv2 as api_gw,
    aws_apigatewayv2_integrations as integrations,
    aws_dynamodb as dynamo_db,
    aws_sns as sns,
    aws_cloudwatch as cloud_watch,
    aws_cloudwatch_actions as actions,
    core
)
from aws_cdk.aws_lambda import Function
from aws_cdk.aws_dynamodb import Table
from aws_cdk.core import Stack, Construct, Duration


class CloudWatchDashboard(Stack):

    def __init__(
        self, scope: Construct, id: str,
        lambda_function: Function,
        dynamodb_table: Table,
        http_api=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.error_topic = sns.Topic(self, 'theBigFanTopic')
        self.dynamodb_table = dynamodb_table
        self.http_api = http_api
        self.lambda_function = lambda_function
        ###
        # Custom Metrics
        ###

        self.api_gw_4xx_error_percentage = cloud_watch.MathExpression(
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
            period=self.five_minutes(),
        )

        # Gather the % of lambda invocations that error in past 5 mins
        self.lambda_error_percentage = cloud_watch.MathExpression(
            expression="e / i * 100",
            label="% of invocations that errored, last 5 mins",
            using_metrics={
                "i": self.add_lambda_function_metric('Invocations'),
                "e": self.add_lambda_function_metric("Errors"),
            },
            period=self.five_minutes(),
        )

        # note: throttled requests are not counted in total num of invocations
        self.lambda_throttled_percentage = self.create_cloudwatch_math_expression(
            label="% of throttled requests, last 30 mins",
            expression="t / (i + t) * 100",
            using_metrics={
                "i": self.add_lambda_function_metric("Invocations"),
                "t": self.add_lambda_function_metric("Throttles"),
            },
        )

        # I think usererrors are at an account level rather than a table level so merging
        # these two metrics until I can get a definitive answer. I think usererrors
        # will always show as 0 when scoped to a table so this is still effectively
        # a system errors count
        self.dynamodb_total_errors = self.cloudwatch_math_sum(
            label="DynamoDB Errors",
            m1=self.dynamodb_table.metric_user_errors(),
            m2=self.dynamodb_table.metric_system_errors_for_operations(),
        )

        # Rather than have 2 alerts, let's create one aggregate metric


        self.create_cloudwatch_alarms()
        self.create_cloudwatch_dashboard()

    def cloudwatch_math_sum(self, label=None, m1=None, m2=None):
        return self.create_cloudwatch_math_expression(
            label=label,
            expression="m1 + m2",
            using_metrics={"m1": m1, "m2": m2},
        )

    def create_cloudwatch_math_expression(self, expression=None, label=None, using_metrics=None):
        return cloud_watch.MathExpression(
            expression=expression,
            label=label,
            using_metrics=using_metrics,
            period=self.five_minutes(),
        )

    def add_cloudwatch_widget(self, title=None, stacked=True, left=None):
        return cloud_watch.GraphWidget(
            title=title, width=8, stacked=stacked, left=left
        )

    def create_cloudwatch_dashboard(self):
        dashboard = cloud_watch.Dashboard(self, id="CloudWatchDashBoard")
        dashboard.add_widgets(
            self.add_cloudwatch_widget(
                title="Requests",
                stacked=False,
                left=[
                    self.add_api_gateway_metric(
                        metric_name="Count",
                        label="# Requests",
                    )
                ]
            ),
            self.add_cloudwatch_widget(
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
            self.add_cloudwatch_widget(
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
            self.add_cloudwatch_widget(
                title="Dynamo Lambda Error %",
                stacked=False,
                left=[self.lambda_error_percentage],
            ),
            self.add_cloudwatch_widget(
                title="Dynamo Lambda Duration",
                left=[
                    self.lambda_function.metric_duration(statistic=statistic)
                    for statistic in ('p50', 'p90', 'p99')
                ],
            ),
            self.add_cloudwatch_widget(
                title="Dynamo Lambda Throttle %",
                left=[self.lambda_throttled_percentage],
                stacked=False,
            ),
            self.add_cloudwatch_widget(
                title="DynamoDB Latency",
                left=[
                    self.dynamodb_successful_request_latency(action) for action in (
                        'GetItem', 'UpdateItem', 'PutItem', 'DeleteItem', 'Query',
                    )
                ],
            ),
            self.add_cloudwatch_widget(
                title="DynamoDB Consumed Read/Write Units",
                stacked=False,
                left=[
                    self.add_dynamodb_metric(metric_name, statistic='avg') for metric_name in (
                        'ConsumedReadCapacityUnits', 'ConsumedWriteCapacityUnits',
                    )
                ]
            ),

            self.add_cloudwatch_widget(
                title="DynamoDB Throttles",
                left=[
                    self.add_dynamodb_metric(metric_name)
                    for metric_name in (
                        'ReadThrottleEvents', 'WriteThrottleEvents',
                    )
                ],
            ),
        )

    def add_dynamodb_metric(self, metric_name, statistic='sum'):
        return self.dynamodb_table.metric(metric_name=metric_name, statistic=statistic)

    def dynamodb_successful_request_latency(self, operation):
        return self.dynamodb_table.metric_successful_request_latency(
            dimensions={
                'TableName': self.dynamodb_table.table_name,
                'Operation': operation,
            }
        )

    def five_minutes(self):
        return Duration.minutes(5)

    def add_lambda_function_metric(self, metric_name):
        return self.lambda_function.metric(metric_name=metric_name, statistic="sum")

    def add_api_gateway_metric(self, metric_name: str = None, label: str = None, period=Duration.seconds(900), statistic: str = 'sum'):
        return cloud_watch.Metric(
            metric_name=metric_name,
            namespace="AWS/ApiGateway",
            dimensions={"ApiId": self.http_api.api_id},
            unit=cloud_watch.Unit.COUNT,
            label=label,
            statistic=statistic,
            period=period,
        )

    def add_cloudwatch_alarm(self, id=None, metric=None, threshold=1):
        return cloud_watch.Alarm(
            self,
            id=id,
            metric=metric,
            threshold=threshold,
            evaluation_periods=6,
            datapoints_to_alarm=1,
            treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING,
        ).add_alarm_action(actions.SnsAction(self.error_topic))

    def create_api_gateway_alarms(self):
        # 4xx are user errors so a large volume indicates a problem
        self.add_cloudwatch_alarm(
            id="API Gateway 4XX Errors > 1%",
            metric=self.api_gw_4xx_error_percentage
        )

        # 5xx are internal server errors so we want 0 of these
        self.add_cloudwatch_alarm(
            id="API Gateway 5XX Errors > 0",
            metric=self.add_api_gateway_metric(
                metric_name="5XXError",
                label="5XX Errors",
                statistic="p99"
            ),
            threshold=0,
        )

        self.add_cloudwatch_alarm(
            id="API p99 latency alarm >= 1s",
            metric=self.add_api_gateway_metric(
                metric_name="Latency",
                label="API GW Latency",
                statistic="p99",
            ),
            threshold=1000,
        )

    def create_lambda_function_alarms(self):
        # Lambda
        # 2% of Dynamo Lambda invocations erroring
        self.add_cloudwatch_alarm(
            id="Dynamo Lambda 2% Error",
            metric=self.lambda_error_percentage,
            threshold=2,
        )

        # 1% of Lambda invocations taking longer than 1 second
        self.add_cloudwatch_alarm(
            id="Dynamo Lambda p99 Long Duration (>1s)",
            metric=self.lambda_function.metric_duration(statistic="p99"),
            threshold=1000,
        )

        # 2% of our lambda invocations are throttled
        self.add_cloudwatch_alarm(
            id="Dynamo Lambda 2% Throttled",
            metric=self.lambda_throttled_percentage,
            threshold=2,
        )

    def create_dynamodb_alarms(self):
        # DynamoDB
        # DynamoDB Interactions are throttled - indicating poorly provisioned
        # Rather than have 2 alerts, let's create one aggregate metric
        self.add_cloudwatch_alarm(
            id="DynamoDB Table Reads/Writes Throttled",
            metric=self.cloudwatch_math_sum(
                label="DynamoDB Throttles",
                m1=self.add_dynamodb_metric('ReadThrottleEvents'),
                m2=self.add_dynamodb_metric('WriteThrottleEvents'),
            ),
        )

    def create_cloudwatch_alarms(self):
        self.create_api_gateway_alarms()
        self.create_lambda_function_alarms()
        self.create_dynamodb_alarms()