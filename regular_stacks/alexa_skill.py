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


        # Allow the skill resource to access the zipped skill package
        role.add_to_policy(
            aws_cdk.aws_iam.PolicyStatement(
                actions=['S3:GetObject'],
                resources=[f'arn:aws:s3:::{asset.s3_bucket_name}/{asset.s3_object_key}']
            )
        )

        # DynamoDB Table
        users_table = aws_cdk.aws_dynamodb.Table(
            self, 'Users',
            partition_key=aws_cdk.aws_dynamodb.Attribute(
                name='userId',
                type=aws_cdk.aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_cdk.aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=aws_cdk.RemovalPolicy.DESTROY
        )

        # install node dependencies for lambdas
        # subprocess.check_call("npm i".split(), cwd=lambda_directory, stdout=subprocess.DEVNULL)
        # subprocess.check_call("npm run build".split(), cwd=lambda_directory, stdout=subprocess.DEVNULL)

        alexa_lambda = aws_cdk.aws_lambda.Function(
            self, "AlexaLambdaHandler",
            runtime=aws_cdk.aws_lambda.Runtime.PYTHON_3_9,
            code=aws_cdk.aws_lambda.Code.from_asset(f"{lambda_directory}/alexa_skill"),
            handler="alexa_skill.handler",
            environment={
                "USERS_TABLE": users_table.table_name
            }
        )

        # grant the lambda role read/write permissions to our table
        users_table.grant_read_write_data(alexa_lambda)

        # create the skill
        skill = aws_cdk.alexa_ask.CfnSkill(
            self, 'the-alexa-skill',
            vendor_id='',
            authentication_configuration={
                'clientId': '',
                'clientSecret': '',
                'refreshToken': ''
            },
            skill_package={
                's3Bucket': asset.s3_bucket_name,
                's3Key': asset.s3_object_key,
                's3BucketRole': role.role_arn,
                'overrides': {
                    'manifest': {
                        'apis': {
                            'custom': {
                                'endpoint': {
                                    'uri': alexa_lambda.function_arn
                                }
                            }
                        }
                    }
                }
            }
        )

        ###
        # Allow the Alexa service to invoke the fulfillment Lambda.
        # In order for the Skill to be created, the fulfillment Lambda
        # must have a permission allowing Alexa to invoke it, this causes
        # a circular dependency and requires the first deploy to allow all
        # Alexa skills to invoke the lambda, subsequent deploys will work
        # when specifying the eventSourceToken
        ###
        alexa_lambda.add_permission(
            'AlexaPermission',
            # eventSourceToken: skill.ref,
            principal=self.get_alexa_service_principal(),
            action='lambda:InvokeFunction'
        )

    @staticmethod
    def get_alexa_service_principal():
        return aws_cdk.aws_iam.ServicePrincipal('alexa-appkit.amazon.com')

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