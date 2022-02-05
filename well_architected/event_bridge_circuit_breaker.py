import os
import lambda_function

from aws_cdk import (
    aws_lambda,
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

        # DynamoDB Table
        # This will store our error records
        # TTL Docs - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/time-to-live-ttl-how-to.html
        error_records = dynamodb.Table(
            self, "CircuitBreaker",
            partition_key=dynamodb.Attribute(
                name="RequestID",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="ExpirationTime",
                type=dynamodb.AttributeType.NUMBER
            ),
            time_to_live_attribute='ExpirationTime'
        )

        # Add an index that lets us query on site url and Expiration Time
        error_records.add_global_secondary_index(
            index_name='UrlIndex',
            partition_key=dynamodb.Attribute(
                name="SiteUrl",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="ExpirationTime",
                type=dynamodb.AttributeType.NUMBER
            )
        )

        aws_integration_lambda = lambda_function.create_python_lambda_function(
            self, function_name='webservice',
            environment_variables=dict(TABLE_NAME=error_records.table_name),
            duration=20,
        )

        # grant the lambda role read/write permissions to our table
        error_records.grant_read_data(aws_integration_lambda)

        # We need to give your lambda permission to put events on our EventBridge
        event_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=['*'],
            actions=['events:PutEvents']
        )
        aws_integration_lambda.add_to_role_policy(event_policy)

        error_lambda = lambda_function.create_python_lambda_function(
            self, function_name='error',
            environment_variables=dict(TABLE_NAME=error_records.table_name),
            duration=3,
        )

        error_records.grant_write_data(error_lambda)

        # Create EventBridge rule to route failures
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

        # defines an API Gateway REST API resource backed by our "integrationaws_lambda" function
        api_gateway.LambdaRestApi(
            self, 'CircuitBreakerGateway',
            handler=aws_integration_lambda
        )