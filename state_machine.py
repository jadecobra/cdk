import aws_cdk
import aws_cdk.aws_apigatewayv2_alpha
import constructs
import lambda_function
import http_api
import api_gateway_cloudwatch
import well_architected

# TODO:
# abstract HTTP API
class StateMachine(well_architected.WellArchitectedFrameworkStack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.output_path = '$.pineappleAnalysis'
        error_topic = self.create_error_topic()
        state_machine = self.create_state_machine(self.create_lambda_function(error_topic))
        http_api = self.create_http_api(error_topic)
        self.create_api_gateway_route(
            api_id=http_api.http_api_id,
            target=self.create_stepfunctions_api_gateway_integration(
                http_api_id=http_api.http_api_id,
                iam_role_arn=self.get_iam_service_role_arn(state_machine.state_machine_arn),
                state_machine_arn=state_machine.state_machine_arn,
            ),
        )

        aws_cdk.CfnOutput(
            self, 'HTTP API URL',
            value=http_api.url
        )

    def create_error_topic(self):
        return aws_cdk.aws_sns.Topic(
            self, 'OrderPizzaErrorTopic',
            display_name='OrderPizzaError'
        )

    def order_failure(self):
        return aws_cdk.aws_stepfunctions.Fail(
            self, 'Sorry, We Dont add Pineapple',
            cause='They asked for Pineapple',
            error='Failed To Make Pizza'
        )

    def order_contains_pineapple(self):
        return aws_cdk.aws_stepfunctions.Condition.boolean_equals(
            f'{self.output_path}.containsPineapple', True
        )

    def order_pizza_task(self, lambda_function):
        return aws_cdk.aws_stepfunctions_tasks.LambdaInvoke(
            self, 'Order Pizza',
            lambda_function=lambda_function,
            input_path='$.flavor',
            result_path=self.output_path,
            payload_response_only=True
        )

    def cook_pizza(self):
        return aws_cdk.aws_stepfunctions.Succeed(
            self, 'Lets make your pizza',
            output_path=self.output_path
        )

    def state_machine_definition(self, lambda_function):
        return (
            aws_cdk.aws_stepfunctions
                .Chain
                .start(self.order_pizza_task(lambda_function))
                .next(
                    aws_cdk.aws_stepfunctions
                        .Choice(self, 'Contains Pineapple?')
                        .when(self.order_contains_pineapple(), self.order_failure())
                        .otherwise(self.cook_pizza())
                )
        )

    def create_lambda_function(self, error_topic):
        return lambda_function.create_python_lambda_function(
            self, function_name='order_pizza',
            error_topic=error_topic
        )

    @staticmethod
    def state_machine_execution_permissions(state_machine_arn):
        return aws_cdk.aws_iam.PolicyDocument(
            statements=[
                aws_cdk.aws_iam.PolicyStatement(
                    actions=["states:StartSyncExecution"],
                    effect=aws_cdk.aws_iam.Effect.ALLOW,
                    resources=[state_machine_arn]
                )
            ]
        )

    def get_iam_service_role_arn(self, state_machine_arn):
        return aws_cdk.aws_iam.Role(
            self, 'StateMachineHttpApiIamRole',
            assumed_by=aws_cdk.aws_iam.ServicePrincipal('apigateway.amazonaws.com'),
            inline_policies={
                "AllowSFNExec": self.state_machine_execution_permissions(state_machine_arn)
            }
        ).role_arn

    def create_state_machine(self, lambda_function):
        return aws_cdk.aws_stepfunctions.StateMachine(
            self, 'StateMachine',
            definition=self.state_machine_definition(lambda_function),
            timeout=aws_cdk.Duration.minutes(5),
            tracing_enabled=True,
            state_machine_type=aws_cdk.aws_stepfunctions.StateMachineType.EXPRESS
        )

    def create_http_api(self, error_topic):
        http_api = aws_cdk.aws_apigatewayv2_alpha.HttpApi(
            self, 'StateMachineHttpApi',
            create_default_stage=True
        )
        api_gateway_cloudwatch.ApiGatewayCloudWatch(
            self, 'StateMachineHttpApiCloudWatch',
            api_id=http_api.http_api_id,
            error_topic=error_topic
        )
        return http_api

    def create_stepfunctions_api_gateway_integration(self, http_api_id=None, iam_role_arn=None, state_machine_arn=None):
        return aws_cdk.aws_apigatewayv2.CfnIntegration(
            self, 'StateMachineHttpApiIntegration',
            api_id=http_api_id,
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
        ).ref

    def create_api_gateway_route(self, api_id=None, target=None):
        return aws_cdk.aws_apigatewayv2.CfnRoute(
            self, 'StateMachineHttpApiDefaultRoute',
            api_id=api_id,
            route_key=aws_cdk.aws_apigatewayv2_alpha.HttpRouteKey.DEFAULT.key,
            target=f'integrations/{target}'
        )