import aws_cdk
import constructs
import lambda_function
import api_gateway_cloudwatch

from aws_cdk import (
    aws_sns,
    aws_stepfunctions,
    aws_stepfunctions_tasks,
    aws_iam,
    aws_apigatewayv2 as api_gateway,
)


class StateMachine(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.pineapple_analysis = '$.pineappleAnalysis'
        error_topic = self.create_error_topic()
        state_machine = self.create_state_machine(self.order_pizza(error_topic))
        http_api_role = self.create_iam_role(state_machine.state_machine_arn)
        http_api = self.create_http_api(error_topic)
        self.create_api_gateway_route(
            api_id=http_api.http_api_id,
            iam_role_arn=http_api_role.role_arn,
            state_machine_arn=state_machine.state_machine_arn
        )

        aws_cdk.CfnOutput(
            self, 'HTTP API URL',
            value=http_api.url
        )

    def create_error_topic(self):
        return aws_sns.Topic(
            self, 'OrderPizzaErrorTopic',
            display_name='OrderPizzaError'
        )

    def order_failure(self):
        return aws_stepfunctions.Fail(
            self, 'Sorry, We Dont add Pineapple',
            cause='They asked for Pineapple',
            error='Failed To Make Pizza'
        )

    def order_contains_pineapple(self):
        return aws_stepfunctions.Condition.boolean_equals(
            f'{self.pineapple_analysis}.containsPineapple', True
        )

    def order_pizza_task(self, lambda_function):
        return aws_stepfunctions_tasks.LambdaInvoke(
            self, 'Order Pizza',
            lambda_function=lambda_function,
            input_path='$.flavor',
            result_path=self.pineapple_analysis,
            payload_response_only=True
        )

    def cook_pizza(self):
        return aws_stepfunctions.Succeed(
            self, 'Lets make your pizza',
            output_path=self.pineapple_analysis
        )

    def state_machine_definition(self, lambda_function):
        return (
            aws_stepfunctions.Chain
                .start(self.order_pizza_task(lambda_function))
                .next(
                    aws_stepfunctions.Choice(self, 'Contains Pineapple?')
                        .when(self.order_contains_pineapple(), self.order_failure())
                        .otherwise(self.cook_pizza())
                )
        )

    def order_pizza(self, error_topic):
        return lambda_function.create_python_lambda_function(
            self, function_name='order_pizza',
            error_topic=error_topic
        )

    @staticmethod
    def state_machine_execution_permissions(state_machine_arn):
        return aws_iam.PolicyDocument(
            statements=[
                aws_iam.PolicyStatement(
                    actions=["states:StartSyncExecution"],
                    effect=aws_iam.Effect.ALLOW,
                    resources=[state_machine_arn]
                )
            ]
        )

    def create_iam_role(self, state_machine_arn):
        return aws_iam.Role(
            self, 'StateMachineHttpApiRole',
            assumed_by=aws_iam.ServicePrincipal('apigateway.amazonaws.com'),
            inline_policies={
                "AllowSFNExec": self.state_machine_execution_permissions(state_machine_arn)
            }
        )

    def create_state_machine(self, lambda_function):
        return aws_stepfunctions.StateMachine(
            self, 'StateMachine',
            definition=self.state_machine_definition(lambda_function),
            timeout=aws_cdk.Duration.minutes(5),
            tracing_enabled=True,
            state_machine_type=aws_stepfunctions.StateMachineType.EXPRESS
        )

    def create_http_api(self, error_topic):
        http_api = api_gateway.HttpApi(
            self, 'StateMachineHttpApi',
            create_default_stage=True
        )
        api_gateway_cloudwatch.ApiGatewayCloudWatch(
            self, 'StateMachineHttpApiCloudWatch',
            api_id=http_api.http_api_id,
            error_topic=error_topic
        )
        return http_api

    def create_stepfunctions_api_gateway_integration(self, api_id=None, iam_role_arn=None, state_machine_arn=None):
        return api_gateway.CfnIntegration(
            self, 'StateMachineHttpApiIntegration',
            api_id=api_id,
            integration_type='AWS_PROXY',
            connection_type='INTERNET',
            integration_subtype='StepFunctions-StartSyncExecution',
            credentials_arn=iam_role_arn,
            request_parameters={
                "Input": "$request.body",
                "StateMachineArn": state_machine_arn,
            },
            payload_format_version="1.0",
            timeout_in_millis=10000
        )

    def create_api_gateway_route(self, api_id=None, iam_role_arn=None, state_machine_arn=None):
        target = self.create_stepfunctions_api_gateway_integration(
            api_id=api_id,
            iam_role_arn=iam_role_arn,
            state_machine_arn=state_machine_arn
        ).ref
        return api_gateway.CfnRoute(
            self, 'StateMachineHttpApiDefaultRoute',
            api_id=api_id,
            route_key=api_gateway.HttpRouteKey.DEFAULT.key,
            target=f'integrations/{target}'
        )