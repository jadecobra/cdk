import aws_cdk
import constructs
import well_architected
import well_architected_api
import well_architected_dynamodb_table
import well_architected_lambda
import aws_cdk.aws_apigatewayv2_integrations_alpha
import aws_cdk.aws_apigatewayv2_alpha
import subprocess


class CircuitBreakerLambda(well_architected.WellArchitectedStack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        dynamodb_table = well_architected_dynamodb_table.DynamoDBTableConstruct(
            self, id,
            partition_key="id",
            error_topic=self.error_topic,
        ).dynamodb_table

        lambda_function = well_architected_lambda.LambdaFunctionConstruct(
            self, 'LambdaFunction',
            error_topic=self.error_topic,
            function_name='circuit_breaker_lambda',
            environment_variables={
                'CIRCUITBREAKER_TABLE': dynamodb_table.table_name
            }
        ).lambda_function

        # grant the lambda role read/write permissions to our table'
        dynamodb_table.grant_read_write_data(lambda_function)


        http_api = well_architected_api.WellArchitectedApi(
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

        aws_cdk.CfnOutput(self, 'HTTP API Url', value=http_api.url)
