import aws_cdk
import constructs
import well_architected
import well_architected_constructs.rest_api_lambda
import well_architected_constructs.lambda_function


class RestApiLambdaStack(well_architected.Stack):

    def __init__(self, scope: constructs.Construct, id: str,
        error_topic:aws_cdk.aws_sns.Topic=None, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.rest_api = well_architected_constructs.rest_api_lambda(
            self, 'RestApiLambda',
        )
