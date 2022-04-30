import aws_cdk
import aws_cdk.aws_apigatewayv2_alpha
import constructs
import well_architected_lambda
import well_architected_api
import well_architected

# TODO:
# abstract HTTP API
class ApiStepFunctions(well_architected.WellArchitectedStack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.result_path = '$.resultPath'
        self.error_topic = self.create_error_topic()
        self.state_machine = self.create_state_machine(self.create_lambda_function(self.error_topic))
        self.http_api = self.create_http_api(self.error_topic)
        self.create_api_gateway_route(
            api_id=self.http_api.http_api_id,
            target=self.create_http_api_stepfunctions_integration(
                http_api_id=self.http_api.http_api_id,
                iam_role_arn=self.get_iam_service_role_arn(self.state_machine.state_machine_arn),
                state_machine_arn=self.state_machine.state_machine_arn,
            ),
        )
        self.rest_api = self.create_rest_api(
            error_topic=self.error_topic,
            state_machine=self.state_machine,
        )

    def create_error_topic(self):
        return aws_cdk.aws_sns.Topic(
            self, 'StateMachineErrorTopic',
            display_name='StateMachineError'
        )

    def failure_message(self):
        return aws_cdk.aws_stepfunctions.Fail(
            self, 'Failed',
            cause='Excpetion',
            error='Error'
        )

    def condition(self):
        return aws_cdk.aws_stepfunctions.Condition.boolean_equals(
            f'{self.result_path}.isValid', True
        )

    def invoke_lambda_function(self, lambda_function):
        return aws_cdk.aws_stepfunctions_tasks.LambdaInvoke(
            self, 'InvokeLambdaFunction',
            lambda_function=lambda_function,
            input_path='$.inputPath',
            result_path=self.result_path,
            payload_response_only=True
        )

    def success_message(self):
        return aws_cdk.aws_stepfunctions.Succeed(
            self, 'Success',
            output_path=self.result_path
        )

    def make_decision(self):
        return (
            aws_cdk.aws_stepfunctions.Choice(
                self, 'isValid?'
            ).when(
                self.condition(),
                self.failure_message()
            ).otherwise(
                self.success_message()
            )
        )

    def state_machine_definition(self, lambda_function):
        return (
            aws_cdk.aws_stepfunctions
                .Chain
                .start(self.invoke_lambda_function(lambda_function))
                .next(self.make_decision())
        )

    def create_lambda_function(self, error_topic):
        return well_architected_lambda.create_python_lambda_function(
            self, function_name='lambda_function',
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
        return well_architected_api.WellArchitectedApi(
            self, 'HttpApi',
            error_topic=error_topic,
            api=aws_cdk.aws_apigatewayv2_alpha.HttpApi(
                self, 'HttpApiStepFunctions',
                create_default_stage=True
            )
        ).api

    def create_rest_api(self, error_topic=None, state_machine=None):
        return well_architected_api.WellArchitectedApi(
            self, 'RestApi',
            error_topic=error_topic,
            api=aws_cdk.aws_apigateway.StepFunctionsRestApi(
                self, 'RestApiStepFunctions',
                state_machine=state_machine,
                deploy=True,
            )
        ).api

    def create_http_api_stepfunctions_integration(self, http_api_id=None, iam_role_arn=None, state_machine_arn=None):
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