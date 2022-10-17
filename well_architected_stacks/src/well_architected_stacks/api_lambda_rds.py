import aws_cdk
import aws_cdk.aws_apigatewayv2_alpha
import aws_cdk.aws_apigatewayv2_integrations_alpha
import constructs
import well_architected_constructs

from . import well_architected_stack


class ApiLambdaRds(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        create_rest_api=False,
        create_http_api=False,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.create_error_topic()
        self.vpc = aws_cdk.aws_ec2.Vpc(self, 'Vpc', max_azs=2)
        db_credentials_secret = self.create_credentials_secret(id)
        self.create_parameter_store_for_db_credentials(db_credentials_secret.secret_arn)
        self.rds_instance = self.create_rds_instance(
            credentials_secret=db_credentials_secret,
            vpc=self.vpc
        )

        self.rds_proxy = self.rds_instance.add_proxy(
            f'{id}-proxy',
            secrets=[db_credentials_secret],
            debug_logging=True,
            vpc=self.vpc,
        )

        self.rds_lambda_construct = well_architected_constructs.api_lambda.ApiLambda(
            self, 'RdsLambda',
            function_name='rds',
            lambda_directory=self.lambda_directory,
            error_topic=self.error_topic,
            vpc=self.vpc,
            environment_variables={
                "PROXY_ENDPOINT": self.rds_proxy.endpoint,
                "RDS_SECRET_NAME": f'{id}-rds-credentials',
            },
            create_http_api=create_http_api,
            create_rest_api=create_rest_api,
        )
        self.lambda_function = self.rds_lambda_construct.lambda_function
        db_credentials_secret.grant_read(self.lambda_function)

        for security_group, description in (
            (self.rds_proxy, 'allow db connection'),
            (self.lambda_function, 'allow lambda connection'),
        ):
            self.rds_instance.connections.allow_from(
                security_group,
                aws_cdk.aws_ec2.Port.tcp(3306),
                description=description
            )

        self.create_cloudwatch_dashboard(
            *self.rds_lambda_construct.lambda_construct.create_cloudwatch_widgets(),
            *self.rds_lambda_construct.api_construct.create_cloudwatch_widgets(),
            # What are the RDS metrics?
        )

    def create_credentials_secret(self, id):
        return aws_cdk.aws_secretsmanager.Secret(
            self, 'DBCredentialsSecret',
            secret_name=f'{id}-rds-credentials',
            generate_secret_string=aws_cdk.aws_secretsmanager.SecretStringGenerator(
                secret_string_template="{\"username\":\"syscdk\"}",
                exclude_punctuation=True,
                include_space=False,
                generate_string_key="password"
            )
        )

    def create_parameter_store_for_db_credentials(self, db_credentials_arn):
        return aws_cdk.aws_ssm.StringParameter(
            self, 'DBCredentialsArn',
            parameter_name='rds-credentials-arn',
            string_value=db_credentials_arn
        )

    def create_rds_instance(self, credentials_secret=None, vpc=None):
        return aws_cdk.aws_rds.DatabaseInstance(
            self, 'DBInstance',
            engine=aws_cdk.aws_rds.DatabaseInstanceEngine.mysql(
                version=aws_cdk.aws_rds.MysqlEngineVersion.VER_5_7_30
            ),
            credentials=aws_cdk.aws_rds.Credentials.from_secret(credentials_secret),
            instance_type=aws_cdk.aws_ec2.InstanceType.of(
                aws_cdk.aws_ec2.InstanceClass.BURSTABLE2,
                aws_cdk.aws_ec2.InstanceSize.SMALL
            ),
            vpc=vpc,
            removal_policy=aws_cdk.RemovalPolicy.DESTROY,
            deletion_protection=False,
        )