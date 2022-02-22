from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigatewayv2 as api_gw,
    aws_apigatewayv2_integrations as integrations,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as secrets,
    aws_ssm as ssm,
    core as cdk
)
import lambda_function


class TheRdsProxyStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(self, 'Vpc', max_azs=2)
        db_credentials_secret = self.create_credentials_secret(id)
        self.create_parameter_store_for_db_credentials(db_credentials_secret.secret_arn)
        rds_instance = self.create_rds_instance(
            credentials_secret=db_credentials_secret,
            vpc=vpc
        )

        rds_proxy = rds_instance.add_proxy(
            f'{id}-proxy',
            secrets=[db_credentials_secret],
            debug_logging=True,
            vpc=vpc,
        )

        rds_lambda = lambda_function.create_python_lambda_function(
            self, function_name='rds',
            vpc=vpc,
            environment_variables={
                "PROXY_ENDPOINT": rds_proxy.endpoint,
                "RDS_SECRET_NAME": f'{id}-rds-credentials',
            }
        )

        db_credentials_secret.grant_read(rds_lambda)

        for security_group, description in (
            (rds_proxy, 'allow db connection'),
            (rds_lambda, 'allow lambda connection'),
        ):
            rds_instance.connections.allow_from(security_group, ec2.Port.tcp(3306), description=description)

        api = api_gw.HttpApi(
            self, 'Endpoint',
            default_integration=integrations.HttpLambdaIntegration(
                'LambdaIntegration', handler=rds_lambda
            )
        )

        cdk.CfnOutput(self, 'HTTP API Url', value=api.url);


    def create_credentials_secret(self, id):
        return secrets.Secret(
            self, 'DBCredentialsSecret',
            secret_name=f'{id}-rds-credentials',
            generate_secret_string=secrets.SecretStringGenerator(
                secret_string_template="{\"username\":\"syscdk\"}",
                exclude_punctuation=True,
                include_space=False,
                generate_string_key="password"
            )
        )

    def create_parameter_store_for_db_credentials(self, db_credentials_arn):
        return ssm.StringParameter(
            self, 'DBCredentialsArn',
            parameter_name='rds-credentials-arn',
            string_value=db_credentials_arn
        )

    def create_rds_instance(self, credentials_secret=None, vpc=None):
        return rds.DatabaseInstance(
            self, 'DBInstance',
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_5_7_30
            ),
            credentials=rds.Credentials.from_secret(credentials_secret),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2,
                ec2.InstanceSize.SMALL
            ),
            vpc=vpc,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            deletion_protection=False,
        )