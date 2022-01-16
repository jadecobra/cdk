from aws_cdk.core import Stack, Construct
from aws_cdk.aws_sns import ITopic
from aws_cdk.aws_sns_subscriptions import LambdaSubscription
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType
from lambda_function import create_python_lambda_function


class DynamoDBFlow(Stack):
    def __init__(self, scope: Construct, id: str, sns_topic: ITopic = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        table = Table(
            self, "Hits",
            partition_key=Attribute(
                name="path", type=AttributeType.STRING
            )
        )

        lambda_function = create_python_lambda_function(
            self, function_name="hit_counter",
            environment_variables={
                "HITS_TABLE_NAME": table.table_name
            }
        )

        table.grant_read_write_data(lambda_function)
        sns_topic.add_subscription(LambdaSubscription(lambda_function))