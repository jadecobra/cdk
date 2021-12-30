from aws_cdk.core import Stack, Construct, Duration
from aws_cdk.aws_lambda import Function, Code, Runtime


class LambdaFunction(Stack):

    def __init__(self, scope: Construct, id: str, function_name=None, environment_variables=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.lambda_function = Function(
            self, "LambdaFunction",
            runtime=Runtime.PYTHON_3_8,
            handler=f'{function_name}.handler',
            code=Code.from_asset("lambda_functions"),
            timeout=Duration.seconds(60),
            environment=environment_variables,
        )

        # lambda_function = _lambda.Function(
        #     self, "DynamoLambdaHandler",
        #     runtime=_lambda.Runtime.NODEJS_12_X,  # execution environment
        #     handler="lambda.handler",  # file is "lambda", function is "handler"
        #     code=_lambda.Code.from_asset("lambda_functions"),  # Code loaded from the lambda dir
        #     environment={
        #         'HITS_TABLE_NAME': dynamodb_table.table_name
        #     }
        # )