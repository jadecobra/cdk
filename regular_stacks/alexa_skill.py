import aws_cdk
import constructs
import well_architected_stacks
import well_architected_constructs
import subprocess
import os


class AlexaSkill(well_architected_stacks.well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        alexa_skills_directory=None,
        lambda_directory=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        asset = self.get_skill_asset(alexa_skills_directory)
        role = self.create_iam_role()
        self.grant_access_to_asset(
            role=role,
            asset=asset
        )

        users_table = self.create_dynamodb_table()
        alexa_lambda = self.create_lambda_function(
            lambda_directory=lambda_directory,
            table_name=users_table.table_name
        )
        users_table.grant_read_write_data(alexa_lambda)

        alexa_skill = self.create_alexa_skill(
            self.get_skill_package(
                lambda_function_arn=alexa_lambda.function_arn,
                s3_key=asset.s3_object_key,
                s3_bucket=asset.s3_bucket_name,
                role_arn=role.role_arn
            )
        )

        self.grant_permission_to_invoke_lambda(
            lambda_function=alexa_lambda,
            event_source_token=alexa_skill.ref,
        )

    def grant_permission_to_invoke_lambda(self, lambda_function=None, event_source_token=None):
        lambda_function.add_permission(
            'AlexaPermission',
            event_source_token=event_source_token, # comment out if first deploy fails with circular dependency
            principal=self.get_alexa_service_principal(),
            action='lambda:InvokeFunction'
        )

    @staticmethod
    def get_alexa_service_principal():
        return aws_cdk.aws_iam.ServicePrincipal('alexa-appkit.amazon.com')

    @staticmethod
    def grant_access_to_asset(role=None, asset=None):
        return role.add_to_policy(
            aws_cdk.aws_iam.PolicyStatement(
                actions=['S3:GetObject'],
                resources=[f'arn:aws:s3:::{asset.s3_bucket_name}/{asset.s3_object_key}']
            )
        )

    def get_skill_asset(self, path):
        return aws_cdk.aws_s3_assets.Asset(
            self, 'SkillAsset', path=path,
        )

    def create_iam_role(self):
        return aws_cdk.aws_iam.Role(
            self, 'Role',
            assumed_by=aws_cdk.aws_iam.CompositePrincipal(
                self.get_alexa_service_principal(),
                aws_cdk.aws_iam.ServicePrincipal('cloudformation.amazonaws.com')
            )
        )

    def create_dynamodb_table(self):
        return aws_cdk.aws_dynamodb.Table(
            self, 'Users',
            partition_key=aws_cdk.aws_dynamodb.Attribute(
                name='userId',
                type=aws_cdk.aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_cdk.aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=aws_cdk.RemovalPolicy.DESTROY
        )

    def create_lambda_function(self, table_name=None, lambda_directory=None):
        return aws_cdk.aws_lambda.Function(
            self, "AlexaLambdaHandler",
            runtime=aws_cdk.aws_lambda.Runtime.PYTHON_3_9,
            code=aws_cdk.aws_lambda.Code.from_asset(f"{lambda_directory}/alexa_skill"),
            handler="alexa_skill.handler",
            environment={
                "USERS_TABLE": table_name
            }
        )

    @staticmethod
    def get_skill_package(s3_bucket=None, s3_key=None, role_arn=None, lambda_function_arn=None):
        return {
            's3Bucket': s3_bucket,
            's3Key': s3_key,
            's3BucketRole': role_arn,
            'overrides': {
                'manifest': {
                    'apis': {
                        'custom': {
                            'endpoint': {
                                'uri': lambda_function_arn
                            }
                        }
                    }
                }
            }
        }

    def create_alexa_skill(self, skill_package):
        return aws_cdk.alexa_ask.CfnSkill(
            self, 'the-alexa-skill',
            skill_package=skill_package,
            vendor_id='',
            authentication_configuration={
                'clientId': '',
                'clientSecret': '',
                'refreshToken': ''
            },
        )