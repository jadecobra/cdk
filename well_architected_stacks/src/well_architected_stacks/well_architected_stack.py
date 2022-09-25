import aws_cdk
import constructs


class Stack(aws_cdk.Stack):

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        lambda_directory='lambda_functions',
        error_topic=None, **kwargs
    ):
        super().__init__(
            scope, id,
            synthesizer=aws_cdk.LegacyStackSynthesizer(),
            **kwargs,
        )
        self.error_topic = error_topic if error_topic else self.create_sns_topic(f'{id}ErrorTopic')
        self.lambda_directory = lambda_directory
        self.vpc = self.get_vpc()

    def create_sns_topic(self, display_name):
        return aws_cdk.aws_sns.Topic(
            self, display_name,
            display_name=display_name,
        )

    def create_lambda_function(self, function_name=None):
        raise NotImplementedError

    def get_vpc(self):
        return aws_cdk.aws_ecs.Vpc.from_lookup(
            self, 'Vpc',
            vpc_id=self.node.try_get_context('vpc_id')
        )