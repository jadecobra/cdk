import aws_cdk
import jsii.errors

from . import sns_topic


class WellArchitectedApp(aws_cdk.App):

    def __init__(
        self,
        lambda_directory='lambda_functions',
        permissions_boundary_name=None,
        application_name=None,
        error_topic=None, **kwargs
    ):
        super().__init__()
        self.lambda_directory = lambda_directory
        self.error_topic = error_topic if error_topic else self.create_sns_topic(f'{application_name}ErrorTopic')
        self.lambda_directory = lambda_directory

        if permissions_boundary_name:
            self.add_permissions_boundary(permissions_boundary_name)

    def create_sns_topic(self, display_name):
        return sns_topic.SnsTopic(
            self, display_name,
            display_name=display_name,
        )

    def create_lambda_function(self, function_name=None):
        raise NotImplementedError

    def add_permissions_boundary(self, policy_name):
        aws_cdk.aws_iam.PermissionsBoundary.of(
            self
        ).apply(
            aws_cdk.aws_iam.ManagedPolicy.from_managed_policy_name(
                self, 'PermissionsBoundary',
                policy_name
            )
        )