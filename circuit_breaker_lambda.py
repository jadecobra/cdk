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

        unreliable_lambda = well_architected_lambda.LambdaFunctionConstruct(
            self, 'LambdaFunction',
            error_topic=self.error_topic,
            function_name='circuit_breaker_lambda/unreliable',
            environment_variables={
                'CIRCUITBREAKER_TABLE': table.table_name
            }
        ).lambda_function

        # grant the lambda role read/write permissions to our table'
        table.grant_read_write_data(unreliable_lambda)

        api = aws_cdk.aws_apigatewayv2_alpha.HttpApi(
            self, 'CircuitBreakerGateway',
            default_integration=integrations.HttpLambdaIntegration(
                'HttpLambdaIntegration', handler=unreliable_lambda
            )
        )

        aws_cdk.CfnOutput(self, 'HTTP API Url', value=api.url)
