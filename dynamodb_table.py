import aws_cdk
import constructs
import aws_cdk.aws_dynamodb as aws_dynamodb
import well_architected

class DynamoDBTableConstruct(well_architected.WellArchitectedFrameworkConstruct):

    def __init__(
        self, scope: constructs.Construct, id: str, error_topic=None,
            partition_key: aws_dynamodb.Attribute=None,
            sort_key: aws_dynamodb.Attribute=None,
            time_to_live_attribute=None,
            **kwargs
    ) -> None:
        super().__init__(scope, id, error_topic=error_topic,
            **kwargs
        )
        self.dynamodb_table = aws_dynamodb.Table(
            self, id,
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            partition_key=partition_key,
            sort_key=sort_key,
            removal_policy=aws_cdk.RemovalPolicy.DESTROY,
            time_to_live_attribute=time_to_live_attribute,
        )
        self.create_user_errors_alarm()
        self.create_throttles_alarm()
        self.create_cloudwatch_dashboard(
            self.create_cloudwatch_widgets()
        )

    def get_dynamodb_metric(self, metric_name, statistic='sum'):
        return self.dynamodb_table.metric(metric_name=metric_name, statistic=statistic)

    def create_throttles_metric(self, action='Read'):
        return self.get_dynamodb_metric(f'{action}ThrottleEvents')

    def create_throttles_alarm(self):
        return self.create_cloudwatch_alarm(
            id="DynamoDB Table Reads/Writes Throttled",
            metric=self.cloudwatch_math_sum(
                label="DynamoDB Throttles",
                m1=self.create_throttles_metric(),
                m2=self.create_throttles_metric('Write'),
            ),
        )

    def create_user_errors_alarm(self):
        return self.create_cloudwatch_alarm(
            id='DynamoDB User Errors > 0',
            metric=self.dynamodb_table.metric_user_errors(),
            threshold=0,
        )

    def create_system_errors_alarm(self):
        # creates jsii.errors.JSIIError: Alarms on math expressions cannot contain more than 10 individual metrics
        return self.create_cloudwatch_alarm(
            id='DynamoDB System Errors > 0',
            metric=self.dynamodb_table.metric_system_errors_for_operations(),
            threshold=0,
        )

    def create_latency_widget(self):
        return self.create_cloudwatch_widget(
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
        return self.create_cloudwatch_widget(
            title="DynamoDB Consumed Read/Write Units",
            stacked=False,
            left=[
                self.get_dynamodb_metric(metric_name, statistic='avg') for metric_name in (
                    'ConsumedReadCapacityUnits', 'ConsumedWriteCapacityUnits',
                )
            ]
        )

    def create_throttles_widget(self):
        return self.create_cloudwatch_widget(
            title="DynamoDB Throttles",
            left=[
                self.create_throttles_metric(),
                self.create_throttles_metric('Write')
            ],
        )

    def create_cloudwatch_widgets(self):
        return  (
            self.create_latency_widget(),
            self.create_read_write_capacity_widget(),
            self.create_throttles_widget(),
        )


class DynamoDBTableStack(aws_cdk.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str, error_topic=None,
            partition_key: aws_dynamodb.Attribute=None,
            sort_key: aws_dynamodb.Attribute=None,
            time_to_live_attribute=None,
            table_name=None,
            **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.dynamodb_table = DynamoDBTableConstruct(
            self, id,
            error_topic=error_topic,
            partition_key=partition_key,
            sort_key=sort_key,
            time_to_live_attribute=time_to_live_attribute,
        ).dynamodb_table