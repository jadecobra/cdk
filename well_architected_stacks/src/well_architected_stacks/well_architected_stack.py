import aws_cdk
import constructs
import jsii.errors


class Stack(aws_cdk.Stack):

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        lambda_directory='lambda_functions',
        permissions_boundary_name=None,
        error_topic=None, **kwargs
    ):
        super().__init__(
            scope, id,
            synthesizer=aws_cdk.LegacyStackSynthesizer(),
            **kwargs,
        )
        self.id = id
        self.lambda_directory = lambda_directory
        self.error_topic = error_topic
        self.permissions_boundary = self.add_permissions_boundary(permissions_boundary_name)

    def create_sns_topic(self, display_name):
        return aws_cdk.aws_sns.Topic(
            self, display_name,
            display_name=display_name,
        )

    def create_error_topic(self, topic_name=None):
        if not self.error_topic:
            if topic_name:
                display_name = topic_name
            else:
                display_name = f'{self.id}ErrorTopic'
            self.error_topic = self.create_sns_topic(display_name)

    def create_lambda_function(self, function_name=None):
        raise NotImplementedError

    def get_vpc(self, vpc_id=None, is_default=None):
        try:
            return aws_cdk.aws_ec2.Vpc.from_lookup(
                self, 'Vpc',
                vpc_id=vpc_id if vpc_id else self.node.try_get_context('vpc_id'),
                is_default=is_default,
            )
        except jsii.errors.JSIIError:
            return aws_cdk.aws_ec2.Vpc(
                self, 'Vpc'
            )

    def add_permissions_boundary(self, policy_name):
        if policy_name:
            return aws_cdk.aws_iam.PermissionsBoundary.of(
                self
            ).apply(
                aws_cdk.aws_iam.ManagedPolicy.from_managed_policy_name(
                    self, 'PermissionsBoundary',
                    policy_name
                )
            )