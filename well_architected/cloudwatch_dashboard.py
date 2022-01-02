import cloudwatch

from aws_cdk.core import Stack, Construct, Duration
from aws_cdk.aws_lambda import Function
from aws_cdk.aws_dynamodb import Table
from aws_cdk.aws_cloudwatch_actions import SnsAction
from aws_cdk.aws_sns import Topic
from aws_cdk.aws_cloudwatch import (
    Alarm, Dashboard, MathExpression, Metric, GraphWidget, TreatMissingData, Unit
)


class CloudWatchDashboard(Stack):

    def __init__(
        self, scope: Construct, id: str,
        lambda_function: Function = None,
        dynamodb_table: Table = None,
        api_id: str = None,
        error_topic: Topic = None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.error_topic = error_topic
        # self.error_topic = Topic(self, 'theBigFanTopic')
        self.dynamodb_table = dynamodb_table
        self.api_id = api_id
        self.lambda_function = lambda_function
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

    def create_lambda_function_metrics(self):
        # Gather the % of lambda invocations that error in past 5 mins
        self.lambda_error_percentage_metric = cloudwatch.create_cloudwatch_math_expression(
            expression="e / invocations * 100",
            label="% of invocations that errored, last 5 mins",
            using_metrics={
                "invocations": self.add_lambda_function_metric('Invocations'),
                "e": self.add_lambda_function_metric("Errors"),
            },
        )

        # note: throttled requests are not counted in total num of invocations
        self.lambda_throttled_percentage_metric = cloudwatch.create_cloudwatch_math_expression(
            label="% of throttled requests, last 30 mins",
            expression="t / (invocations + t) * 100",
            using_metrics={
                "invocations": self.add_lambda_function_metric("Invocations"),
                "t": self.add_lambda_function_metric("Throttles"),
            },
        )



    def create_metrics(self):
        self.create_api_gateway_metrics()
        self.create_lambda_function_metrics()
        self.create_dynamodb_metrics()

    @staticmethod
    def create_cloudwatch_widget(title=None, stacked=True, left=None):
        return GraphWidget(
            title=title, width=8, stacked=stacked, left=left
        )

    def create_cloudwatch_dashboard(self):
        self.dashboard = Dashboard(self, "CloudWatchDashBoard")
        self.dashboard.add_widgets(
            self.create_cloudwatch_widget(
                title="Requests",
                stacked=False,
                left=[
                    self.add_api_gateway_metric(
                        metric_name="Count",
                        label="# Requests",
                    )
                ]
            ),
            self.create_cloudwatch_widget(
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
            self.create_cloudwatch_widget(
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
            self.create_cloudwatch_widget(
                title="Dynamo Lambda Error %",
                stacked=False,
                left=[self.lambda_error_percentage_metric],
            ),
            self.create_cloudwatch_widget(
                title="Dynamo Lambda Duration",
                left=[
                    self.lambda_function.metric_duration(statistic=statistic)
                    for statistic in ('p50', 'p90', 'p99')
                ],
            ),
            self.create_cloudwatch_widget(
                title="Dynamo Lambda Throttle %",
                left=[self.lambda_throttled_percentage_metric],
                stacked=False,
            ),
            self.create_dynamodb_latency_widget(),
            self.create_dynamodb_read_write_capacity_widget(),
            self.create_dynamodb_throttles_widget(),
        )

    def five_minutes(self):
        return Duration.minutes(5)

    def add_lambda_function_metric(self, metric_name):
        return self.lambda_function.metric(metric_name=metric_name, statistic="sum")

    def add_api_gateway_metric(self, metric_name: str = None, label: str = None, period=Duration.seconds(900), statistic: str = 'sum'):
        return Metric(
            metric_name=metric_name,
            namespace="AWS/ApiGateway",
            dimensions={
                "ApiId": self.api_id,
            },
            unit=Unit.COUNT,
            label=label,
            statistic=statistic,
            period=period,
        )

    def add_cloudwatch_alarm(self, id=None, metric=None, threshold=1):
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

    def create_api_gateway_alarms(self):
        # 4xx are user errors so a large volume indicates a problem
        self.add_cloudwatch_alarm(
            id="API Gateway 4XX Errors > 1%",
            metric=self.api_gateway_4xx_error_percentage
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
            metric=self.lambda_error_percentage_metric,
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
            metric=self.lambda_throttled_percentage_metric,
            threshold=2,
        )

    def add_dynamodb_metric(self, metric_name, statistic='sum'):
        return self.dynamodb_table.metric(metric_name=metric_name, statistic=statistic)

    def create_dynamodb_metrics(self):
        # I think usererrors are at an account level rather than a table level so merging
        # these two metrics until I can get a definitive answer. I think usererrors
        # will always show as 0 when scoped to a table so this is still effectively
        # a system errors count
        self.dynamodb_total_errors_metric = cloudwatch.cloudwatch_math_sum(
            label="DynamoDB Errors",
            m1=self.dynamodb_table.metric_user_errors(),
            m2=self.dynamodb_table.metric_system_errors_for_operations(),
        )

    def create_dynamodb_alarms(self):
        # There should be 0 DynamoDB errors
        # Alarms on math expressions cannot contain more than 10 individual metrics
        # self.add_cloudwatch_alarm(
        #     id="DynamoDB Errors > 0",
        #     metric=self.dynamodb_total_errors,
        #     threshold=0,
        # )
        return

    def create_dynamodb_latency_widget(self):
        return self.create_cloudwatch_widget(
            title="DynamoDB Latency",
            left=[
                self.dynamodb_table.metric_successful_request_latency(
                    dimensions={
                        'TableName': self.dynamodb_table.table_name,
                        'Operation': action,
                    }
                ) for action in (
                    'GetItem', 'UpdateItem', 'PutItem', 'DeleteItem', 'Query',
                )
            ],
        )

    def create_dynamodb_read_write_capacity_widget(self):
        return self.create_cloudwatch_widget(
            title="DynamoDB Consumed Read/Write Units",
            stacked=False,
            left=[
                self.add_dynamodb_metric(metric_name, statistic='avg') for metric_name in (
                    'ConsumedReadCapacityUnits', 'ConsumedWriteCapacityUnits',
                )
            ]
        )

    def create_dynamodb_throttles_widget(self):
        # DynamoDB Interactions are throttled - indicaticating poor provisioning
        # Rather than have 2 alerts, let's create one aggregate metric
        self.add_cloudwatch_alarm(
            id="DynamoDB Table Reads/Writes Throttled",
            metric=cloudwatch.cloudwatch_math_sum(
                label="DynamoDB Throttles",
                m1=self.add_dynamodb_metric('ReadThrottleEvents'),
                m2=self.add_dynamodb_metric('WriteThrottleEvents'),
            ),
        )
        return self.create_cloudwatch_widget(
            title="DynamoDB Throttles",
            left=[
                self.add_dynamodb_metric(metric_name)
                for metric_name in (
                    'ReadThrottleEvents', 'WriteThrottleEvents',
                )
            ],
        )

    def create_cloudwatch_alarms(self):
        self.create_api_gateway_alarms()
        self.create_lambda_function_alarms()
        self.create_dynamodb_alarms()