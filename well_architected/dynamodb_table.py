from aws_cdk.core import Stack, Construct
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType, BillingMode

class DynamoDBTable(Stack):

    def __init__(
        self, scope: Construct, id: str, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.dynamodb_table = Table(
            self, "Hits",
            billing_mode=BillingMode.PAY_PER_REQUEST,
            partition_key=Attribute(
                name="path",
                type=AttributeType.STRING
            ),
        )