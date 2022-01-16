from aws_cdk.core import Stack, Construct
from aws_cdk.aws_sns import Topic


class SnsTopic(Stack):

    def __init__(self, scope: Construct, id: str, display_name=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.topic = Topic(
            self, id,
            display_name=display_name
        )