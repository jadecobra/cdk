import os
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
import jsii


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
        ###
        # Custom Metrics
        ###

        self.api_gw_4xx_error_percentage = cloud_watch.MathExpression(
            expression="m1/m2*100",
            label="% API Gateway 4xx Errors",
            using_metrics={
                "m1": self.metric_for_api_gw(
                    http_api.http_api_id,
                    '4XXError',
                    '4XX Errors',
                    'sum'
                ),
                "m2": self.metric_for_api_gw(
                    http_api.http_api_id,
                    'Count',
                    '# Requests',
                    'sum'
                ),
            },
            period=self.five_minutes()
        )

        # Gather the % of lambda invocations that error in past 5 mins
        self.lambda_error_percentage = cloud_watch.MathExpression(
            expression="e / i * 100",
            label="% of invocations that errored, last 5 mins",
            using_metrics={
                "i": lambda_function.metric(
                    metric_name="Invocations", statistic="sum"
                ),
                "e": lambda_function.metric(
                    metric_name="Errors", statistic="sum"
                ),
            },
            period=self.five_minutes()
        )

        # note: throttled requests are not counted in total num of invocations
        self.lambda_throttled_percentage = cloud_watch.MathExpression(
            expression="t / (i + t) * 100",
            label="% of throttled requests, last 30 mins",
            using_metrics={
                "i": lambda_function.metric(
                    metric_name="Invocations", statistic="sum"
                ),
                "t": lambda_function.metric(
                    metric_name="Throttles", statistic="sum"
                ),
            },
            period=self.five_minutes()
        )

        # I think usererrors are at an account level rather than a table level so merging
        # these two metrics until I can get a definitive answer. I think usererrors
        # will always show as 0 when scoped to a table so this is still effectively
        # a system errors count
        self.dynamodb_total_errors = cloud_watch.MathExpression(
            expression="m1 + m2",
            label="DynamoDB Errors",
            using_metrics={
                "m1": self.dynamodb_table.metric_user_errors(),
                "m2": self.dynamodb_table.metric_system_errors_for_operations(),
            },
            period=self.five_minutes()
        )

        # Rather than have 2 alerts, let's create one aggregate metric
        self.dynamodb_throttles = cloud_watch.MathExpression(
            expression="m1 + m2",
            label="DynamoDB Throttles",
            using_metrics={
                "m1": self.dynamodb_table.metric(
                    metric_name="ReadThrottleEvents", statistic="sum"
                ),
                "m2": self.dynamodb_table.metric(
                    metric_name="WriteThrottleEvents", statistic="sum"
                ),
            },
            period=self.five_minutes()
        )
        ###
        # Alarms
        ###

        # Api Gateway

        # 4xx are user errors so a large volume indicates a problem
        cloud_watch.Alarm(
            self, id="API Gateway 4XX Errors > 1%",
            metric=self.api_gw_4xx_error_percentage,
            threshold=1,
            evaluation_periods=6,
            datapoints_to_alarm=1,
            treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING
        ).add_alarm_action(actions.SnsAction(self.error_topic))

        # 5xx are internal server errors so we want 0 of these
        cloud_watch.Alarm(
            self, id="API Gateway 5XX Errors > 0",
            metric=self.metric_for_api_gw(api_id=http_api.http_api_id,
                                        metric_name="5XXError",
                                        label="5XX Errors",
                                        stat="p99"),
            threshold=0,
            period=self.five_minutes(),
            evaluation_periods=6,
            datapoints_to_alarm=1,
            treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING
        ).add_alarm_action(actions.SnsAction(self.error_topic))

        cloud_watch.Alarm(
            self, id="API p99 latency alarm >= 1s",
            metric=self.metric_for_api_gw(api_id=http_api.http_api_id,
                                        metric_name="Latency",
                                        label="API GW Latency",
                                        stat="p99"),
            threshold=1000,
            period=self.five_minutes(),
            evaluation_periods=6,
            datapoints_to_alarm=1,
            treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING
        ).add_alarm_action(actions.SnsAction(self.error_topic))

        # Lambda

        # 2% of Dynamo Lambda invocations erroring
        cloud_watch.Alarm(
            self, id="Dynamo Lambda 2% Error",
            metric=self.lambda_error_percentage,
            threshold=2,
            evaluation_periods=6,
            datapoints_to_alarm=1,
            treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING
        ).add_alarm_action(actions.SnsAction(self.error_topic))

        # 1% of Lambda invocations taking longer than 1 second
        cloud_watch.Alarm(
            self, id="Dynamo Lambda p99 Long Duration (>1s)",
            metric=lambda_function.metric_duration(),
            period=self.five_minutes(),
            threshold=1000,
            evaluation_periods=6,
            datapoints_to_alarm=1,
            statistic="p99",
            treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING
        ).add_alarm_action(actions.SnsAction(self.error_topic))

        # 2% of our lambda invocations are throttled
        cloud_watch.Alarm(
            self, id="Dynamo Lambda 2% Throttled",
            metric=self.lambda_throttled_percentage,
            threshold=2,
            evaluation_periods=6,
            datapoints_to_alarm=1,
            treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING
        ).add_alarm_action(actions.SnsAction(self.error_topic))

        # DynamoDB

        # DynamoDB Interactions are throttled - indicated poorly provisioned
        cloud_watch.Alarm(
            self, id="DynamoDB Table Reads/Writes Throttled",
            metric=self.dynamodb_throttles,
            threshold=1,
            evaluation_periods=6,
            datapoints_to_alarm=1,
            treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING
        ).add_alarm_action(actions.SnsAction(self.error_topic))

        # There should be 0 DynamoDB errors
        # cloud_watch.Alarm(self,
        #                   id="DynamoDB Errors > 0",
        #                   metric=dynamo_db_total_errors,
        #                   threshold=0,
        #                   evaluation_periods=6,
        #                   datapoints_to_alarm=1,
        #                   treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING) \
        #     .add_alarm_action(actions.SnsAction(error_topic))

        dashboard = cloud_watch.Dashboard(self, id="CloudWatchDashBoard")
        dashboard.add_widgets(
            cloud_watch.GraphWidget(title="Requests",
                width=8,
                left=[
                    self.metric_for_api_gw(
                        api_id=http_api.http_api_id,
                        metric_name="Count",
                        label="# Requests",
                        stat="sum"
                    )
                ]
            ),
            cloud_watch.GraphWidget(
                title="API GW Latency",
                width=8,
                stacked=True,
                left=[
                    self.metric_for_api_gw(
                        api_id=http_api.http_api_id,
                        metric_name="Latency",
                        label="API Latency p50",
                        stat="p50"
                    ),
                    self.metric_for_api_gw(
                        api_id=http_api.http_api_id,
                        metric_name="Latency",
                        label="API Latency p90",
                        stat="p90"
                    ),
                    self.metric_for_api_gw(
                        api_id=http_api.http_api_id,
                        metric_name="Latency",
                        label="API Latency p99",
                        stat="p99"
                    )
                ]
            ),
            cloud_watch.GraphWidget(
                title="API GW Errors",
                width=8,
                stacked=True,
                left=[
                    self.metric_for_api_gw(
                        api_id=http_api.http_api_id,
                        metric_name="4XXError",
                        label="4XX Errors",
                        stat="sum"
                    ),
                    self.metric_for_api_gw(
                        api_id=http_api.http_api_id,
                        metric_name="5XXError",
                        label="5XX Errors",
                        stat="sum"
                    )
                ]
            ),
            cloud_watch.GraphWidget(
                title="Dynamo Lambda Error %",
                width=8,
                left=[self.lambda_error_percentage]
            ),
            cloud_watch.GraphWidget(
                title="Dynamo Lambda Duration",
                width=8,
                stacked=True,
                left=[
                    lambda_function.metric_duration(statistic="p50"),
                    lambda_function.metric_duration(statistic="p90"),
                    lambda_function.metric_duration(statistic="p99")
                ]
            ),
            cloud_watch.GraphWidget(
                title="Dynamo Lambda Throttle %",
                width=8,
                left=[self.lambda_throttled_percentage]
            ),
            cloud_watch.GraphWidget(
                title="DynamoDB Latency",
                width=8,
                stacked=True,
                left=[
                    self.dynamodb_successful_request_latency(action) for action in (
                        'GetItem', 'UpdateItem', 'PutItem', 'DeleteItem', 'Query'
                    )
                ],
            ),
            cloud_watch.GraphWidget(
                title="DynamoDB Consumed Read/Write Units",
                width=8,
                stacked=False,
                left=[
                    self.dynamodb_table.metric(metric_name="ConsumedReadCapacityUnits"),
                    self.dynamodb_table.metric(metric_name="ConsumedWriteCapacityUnits")
                ]
            ),
            cloud_watch.GraphWidget(
                title="DynamoDB Throttles",
                width=8,
                stacked=True,
                left=[
                    self.dynamodb_table.metric(
                        metric_name="ReadThrottleEvents",
                        statistic="sum"
                    ),
                    self.dynamodb_table.metric(
                        metric_name="WriteThrottleEvents",
                        statistic="sum"
                    )
                ]
            ),
        )

    def dynamodb_successful_request_latency(self, operation):
        return self.dynamodb_table.metric_successful_request_latency(
            dimensions={
                'TableName': self.dynamodb_table.table_name,
                'Operation': operation
            }
        )

    def five_minutes(self):
        return Duration.minutes(5)

    @jsii.implements(cloud_watch.IMetric)
    def metric_for_api_gw(self, api_id: str, metric_name: str, label: str, stat: str = 'avg'):
        return self.build_metric(metric_name, "AWS/ApiGateway", {"ApiId": api_id}, cloud_watch.Unit.COUNT, label, stat)

    @staticmethod
    def build_metric(metric_name: str, name_space: str, dimensions, unit: cloud_watch.Unit, label: str,
                     stat: str = 'avg', period: int = 900):
        return cloud_watch.Metric(metric_name=metric_name,
                                  namespace=name_space,
                                  dimensions=dimensions,
                                  unit=unit,
                                  label=label,
                                  statistic=stat,
                                  period=Duration.seconds(period))