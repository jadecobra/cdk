import aws_cdk
import constructs
import jsii.errors


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

    def create_sns_topic(self, display_name):
        return aws_cdk.aws_sns.Topic(
            self, display_name,
            display_name=display_name,
        )

    def create_lambda_function(self, function_name=None):
        raise NotImplementedError

    def get_vpc(self, vpc_id=None):
        try:
            return aws_cdk.aws_ec2.Vpc.from_lookup(
                self, 'Vpc',
                vpc_id=vpc_id if vpc_id else self.node.try_get_context('vpc_id')
            )
        except jsii.errors.JSIIError:
            return aws_cdk.aws_ec2.Vpc(
                self, 'Vpc'
            )