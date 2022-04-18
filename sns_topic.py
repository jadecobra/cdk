import aws_cdk
import constructs


class SnsTopic(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, display_name=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.topic = aws_cdk.aws_sns.Topic(
            self, id,
            display_name=display_name
        )