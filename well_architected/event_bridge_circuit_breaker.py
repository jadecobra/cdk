import os
import lambda_function

from aws_cdk import (
    aws_apigateway as api_gateway,
    aws_dynamodb as dynamodb,
    aws_events,
    aws_events_targets as targets,
    aws_iam as iam,
    core as cdk,
)

class EventBridgeCircuitBreaker(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        expiration_time_sort_key = dynamodb.Attribute(
            name="ExpirationTime",
            type=dynamodb.AttributeType.NUMBER
        )

        error_records = dynamodb.Table(
            self, "CircuitBreaker",
            partition_key=dynamodb.Attribute(
                name="RequestID",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=expiration_time_sort_key,
            time_to_live_attribute='ExpirationTime'
        )

        error_records.add_global_secondary_index(
            index_name='UrlIndex',
            partition_key=dynamodb.Attribute(
                name="SiteUrl",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=expiration_time_sort_key
        )

        environment_variables = dict(ERROR_RECORDS=error_records.table_name)

        aws_integration_lambda = lambda_function.create_python_lambda_function(
            self, function_name='webservice',
            environment_variables=environment_variables,
            duration=20,
        )

        error_lambda = lambda_function.create_python_lambda_function(
            self, function_name='error',
            environment_variables=environment_variables,
            duration=3,
        )

        error_records.grant_read_data(aws_integration_lambda)
        error_records.grant_write_data(error_lambda)

        aws_integration_lambda.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                resources=['*'],
                actions=['events:PutEvents']
            )
        )

        error_rule = aws_events.Rule(
            self, 'webserviceErrorRule',
            description='Failed Webservice Call',
            event_pattern=aws_events.EventPattern(
                source=['cdkpatterns.eventbridge.circuitbreaker'],
                detail_type=['httpcall'],
                detail={
                    "status": ["fail"]
                }
            )
        )

        error_rule.add_target(targets.LambdaFunction(handler=error_lambda))

        api_gateway.LambdaRestApi(
            self, 'CircuitBreakerGateway',
            handler=aws_integration_lambda
        )