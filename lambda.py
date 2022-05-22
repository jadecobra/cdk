import constructs
import aws_cdk

class LambdaFunctionStack(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str,
        function_name=None, environment_variables=None, error_topic:aws_cdk.aws_sns.ITopic=None,
        handler_name=None,
        **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.lambda_function = create_python_lambda_function(
            self, function_name=function_name,
            environment_variables=environment_variables,
            error_topic=error_topic,
            handler_name=handler_name,
        )