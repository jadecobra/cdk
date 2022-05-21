import aws_cdk
import constructs
import well_architected
import well_architected_dynamodb_table
import well_architected_lambda
import aws_cdk.aws_apigatewayv2_integrations_alpha as integrations
import aws_cdk.aws_apigatewayv2_alpha
import subprocess



class CircuitBreakerLambda(well_architected.WellArchitectedStack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        table = well_architected_dynamodb_table.DynamoDBTableConstruct(
            self, id,
            partition_key="id",
        ).dynamodb_table

        # install node dependencies for lambdas
        # lambda_folder = os.path.dirname(os.path.realpath(__file__)) + "/lambda_functions"
        # subprocess.check_call("npm i".split(), cwd=lambda_folder, stdout=subprocess.DEVNULL)
        # subprocess.check_call("npm run build".split(), cwd=lambda_folder, stdout=subprocess.DEVNULL)

        # defines an AWS Lambda resource with unreliable code
        unreliable_lambda = aws_cdk.aws_lambda.Function(
            self, "unreliable",
            runtime=aws_cdk.aws_lambda.Runtime.NODEJS_12_X,
            handler="unreliable.handler",
            code=aws_cdk.aws_lambda.Code.from_asset("lambda_functions/unreliable"),
            environment={
                'CIRCUITBREAKER_TABLE': table.table_name
            }
        )

        # grant the lambda role read/write permissions to our table'
        table.grant_read_write_data(unreliable_lambda)

        # defines an API Gateway Http API resource backed by our "dynamoLambda" function.
        api = aws_cdk.aws_apigatewayv2_alpha.HttpApi(
            self, 'CircuitBreakerGateway',
            default_integration=integrations.HttpLambdaIntegration(
                'HttpLambdaIntegration', handler=unreliable_lambda
            )
        )

        aws_cdk.CfnOutput(self, 'HTTP API Url', value=api.url)
