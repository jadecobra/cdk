import aws_cdk
import constructs
import aws_cdk.aws_sns as aws_sns
import aws_cdk.aws_sns_subscriptions as aws_sns_subscriptions
import aws_cdk.aws_dynamodb as aws_dynamodb
import well_architected_constructs.lambda_function
import well_architected_constructs.dynamodb_table

class DynamoDBFlow(aws_cdk.Stack):
    def __init__(self, scope: constructs.Construct, id: str, sns_topic: aws_sns.ITopic = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        table = well_architected_constructs.dynamodb_table.DynamoDBTableConstruct(
            self, "Hits",
            partition_key=aws_dynamodb.Attribute(
                name="path", type=aws_dynamodb.AttributeType.STRING
            )
        ).dynamodb_table

        self.lambda_function = well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name="hit_counter",
            environment_variables={
                "HITS_TABLE_NAME": table.table_name
            }
        )

        table.grant_read_write_data(self.lambda_function)
        sns_topic.add_subscription(
            aws_sns_subscriptions.LambdaSubscription(
                
                self.lambda_function

        ))