import aws_cdk
import constructs
import well_architected_stacks
import well_architected_constructs


class AlexaSkill(well_architected_stacks.well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        alexa_skills_directory=None,
        lambda_directory=None,
        **kwargs
    ) -> None:
        super().__init__(
            scope, id,
            lambda_directory=lambda_directory,
            **kwargs
        )
        asset = self.get_skill_asset(alexa_skills_directory)
        role = self.create_iam_role()
        self.grant_access_to_asset(
            role=role,
            s3_bucket_name=asset.s3_bucket_name,
            s3_object_key=asset.s3_object_key,
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
            principal=self.alexa_service_principal(),
            action='lambda:InvokeFunction'
        )

    @staticmethod
    def service_principal(principal):
        return aws_cdk.aws_iam.ServicePrincipal(principal)

    def alexa_service_principal(self):
        return self.service_principal('alexa-appkit.amazon.com')

    @staticmethod
    def grant_access_to_asset(role=None, s3_bucket_name=None, s3_object_key=None):
        return role.add_to_policy(
            aws_cdk.aws_iam.PolicyStatement(
                actions=['S3:GetObject'],
                resources=[f'arn:aws:s3:::{s3_bucket_name}/{s3_object_key}']
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
                self.alexa_service_principal(),
                self.service_principal('cloudformation.amazonaws.com')
            )
        )

    def create_dynamodb_table(self):
        return well_architected_constructs.dynamodb_table.DynamodbTableConstruct(
            self, 'DynamoDbTable',
            partition_key='userId',
        ).dynamodb_table

    def create_lambda_function(self, table_name=None, lambda_directory=None):
        return well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, 'LambdaFunction',
            function_name='alexa_skill',
            lambda_directory=self.lambda_directory,
            duration=60,
            environment_variables={
                "USERS_TABLE": table_name
            }
        ).lambda_function

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
            self, 'AlexaSkill',
            skill_package=skill_package,
            vendor_id='',
            authentication_configuration={
                'clientId': '',
                'clientSecret': '',
                'refreshToken': ''
            },
        )