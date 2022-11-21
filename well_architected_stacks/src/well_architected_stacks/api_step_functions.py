import aws_cdk
import aws_cdk.aws_apigatewayv2_alpha
import constructs
import well_architected_constructs

from . import well_architected_stack


class ApiStepFunctionsStack(well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.result_path = '$.resultPath'
        self.lambda_construct = self.create_lambda_construct()

        self.api_step_functions = well_architected_constructs.api_step_functions.ApiStepFunctions(
            self, 'ApiStepFunctions',
            create_http_api=self.create_http_api,
            create_rest_api=self.create_rest_api,
            state_machine_definition=self.state_machine_definition(
                self.lambda_construct.lambda_function
            ),
        )
        self.state_machine = self.api_step_functions.state_machine
        self.create_cloudwatch_dashboard(
            *self.lambda_construct.create_cloudwatch_widgets(),
            *self.api_step_functions.api_construct.create_cloudwatch_widgets(),
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

    def create_lambda_construct(self):
        return well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name='lambda_function',
            error_topic=self.error_topic,
            lambda_directory=self.lambda_directory,
        )
