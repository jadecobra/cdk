import aws_cdk
import constructs
import well_architected
import well_architected_api
import well_architected_dynamodb_table
import well_architected_lambda
import aws_cdk.aws_apigatewayv2_integrations_alpha
import aws_cdk.aws_apigatewayv2_alpha


class CircuitBreakerLambda(well_architected.WellArchitectedStack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        dynamodb_table = self.create_dynamodb_table(id)
        lambda_function = self.create_lambda_function(dynamodb_table.table_name)
        dynamodb_table.grant_read_write_data(lambda_function)
        aws_cdk.CfnOutput(self, 'HTTP API Url', value=self.create_http_api(lambda_function).url)

    def create_dynamodb_table(self, id):
        return well_architected_dynamodb_table.DynamoDBTableConstruct(
            self, id,
            partition_key="id",
            error_topic=self.error_topic,
        ).dynamodb_table

    def create_lambda_function(self, table_name):
        return well_architected_lambda.LambdaFunctionConstruct(
            self, 'LambdaFunction',
            error_topic=self.error_topic,
            function_name='circuit_breaker_lambda',
            environment_variables={
                'CIRCUITBREAKER_TABLE': table_name
            }
        ).lambda_function

    def create_http_api(self, lambda_function):
        return well_architected_api.WellArchitectedApi(
            self, 'HttpApiGateway',
            error_topic=self.error_topic,
            api=aws_cdk.aws_apigatewayv2_alpha.HttpApi(
                self, 'HttpApi',
                default_integration=aws_cdk.aws_apigatewayv2_integrations_alpha.HttpLambdaIntegration(
                    'LambdaFunction',
                    handler=lambda_function
                ),
            )
        ).api