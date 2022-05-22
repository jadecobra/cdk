import aws_cdk
import constructs


class DynamoDBTableStack(aws_cdk.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str, error_topic=None,
            partition_key: aws_cdk.aws_dynamodb.Attribute=None,
            sort_key: aws_cdk.aws_dynamodb.Attribute=None,
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