from aws_cdk.core import Stack, Construct
import cloudwatch
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType, BillingMode

class DynamoDBTable(Stack):

    def __init__(
        self, scope: Construct, id: str, error_topic=None, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.error_topic = error_topic
        self.dynamodb_table = Table(
            self, "Hits",
            billing_mode=BillingMode.PAY_PER_REQUEST,
            partition_key=Attribute(
                name="path",
                type=AttributeType.STRING
            ),
        )
        # self.create_total_errors_alarm() # too many metrics for alarm
        self.create_throttles_alarm()
        self.dynamodb_cloudwatch_widgets = self.create_cloudwatch_widgets()

    def get_dynamodb_metric(self, metric_name, statistic='sum'):
        return self.dynamodb_table.metric(metric_name=metric_name, statistic=statistic)

    def create_latency_widget(self):
        return cloudwatch.create_cloudwatch_widget(
            title="DynamoDB Latency",
            left=[
                self.dynamodb_table.metric_successful_request_latency(
                    dimensions_map={
                        'TableName': self.dynamodb_table.table_name,
                        'Operation': action,
                    }
                ) for action in (
                    'GetItem', 'UpdateItem', 'PutItem', 'DeleteItem', 'Query',
                )
            ],
        )

    def create_read_write_capacity_widget(self):
        return cloudwatch.create_cloudwatch_widget(
            title="DynamoDB Consumed Read/Write Units",
            stacked=False,
            left=[
                self.get_dynamodb_metric(metric_name, statistic='avg') for metric_name in (
                    'ConsumedReadCapacityUnits', 'ConsumedWriteCapacityUnits',
                )
            ]
        )

    def create_throttles_metric(self, action='Read'):
        return self.get_dynamodb_metric(f'{action}ThrottleEvents')

    def create_throttles_widget(self):
        return cloudwatch.create_cloudwatch_widget(
            title="DynamoDB Throttles",
            left=[
                self.create_throttles_metric(),
                self.create_throttles_metric('Write')
            ],
        )

    def create_throttles_alarm(self):
        return cloudwatch.create_cloudwatch_alarm(
            self, id="DynamoDB Table Reads/Writes Throttled",
            metric=cloudwatch.cloudwatch_math_sum(
                label="DynamoDB Throttles",
                m1=self.create_throttles_metric(),
                m2=self.create_throttles_metric('Write'),
            ),
            error_topic=self.error_topic,
        )

    def create_total_errors_alarm(self):
        # I think usererrors are at an account level rather than a table level so merging
        # these two metrics until I can get a definitive answer. I think usererrors
        # will always show as 0 when scoped to a table so this is still effectively
        # a system errors count

        # There should be 0 DynamoDB errors
        # Alarms on math expressions cannot contain more than 10 individual metrics
        # It appears the sume of user errors and system errors is more than 10 metrics
        cloudwatch.create_cloudwatch_alarm(
            self, id="DynamoDB Errors > 0",
            metric=cloudwatch.cloudwatch_math_sum(
                label="DynamoDB Errors",
                m1=self.dynamodb_table.metric_user_errors(),
                m2=self.dynamodb_table.metric_system_errors_for_operations(),
            ),
            threshold=0,
        )

    def create_cloudwatch_widgets(self):
        return [
            widget for widget in (
                self.create_latency_widget(),
                self.create_read_write_capacity_widget(),
                self.create_throttles_widget(),
            )
        ]