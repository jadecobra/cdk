import aws_cdk.core
import aws_cdk.aws_lambda
import aws_cdk.aws_sam


class LambdaPowerTuner(aws_cdk.core.Stack):

    def __init__(self, scope: aws_cdk.core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        example_lambda_function = aws_cdk.aws_lambda.Function(
            self, "exampleLambda",
            runtime=aws_cdk.aws_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=aws_cdk.aws_lambda.Code.from_inline(
                "def handler(event, context): return 'hi'"),
        )

        # uncomment to only allow this power tuner to manipulate this defined function
        # lambda_resource = example_lamdba.function_arn

        # Output the Lambda function ARN in the deploy logs to ease testing
        aws_cdk.core.CfnOutput(self, 'LambdaARN', value=example_lambda_function.function_arn)

        # Deploy the aws-lambda-powertuning application from the Serverless Application Repository
        # https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:451282441545:applications~aws-lambda-power-tuning
        aws_cdk.aws_sam.CfnApplication(self, 'powerTuner', location={
            "applicationId": "arn:aws:serverlessrepo:us-east-1:451282441545:applications/aws-lambda-power-tuning",
            "semanticVersion": "3.4.0"
        }, parameters={
            "lambdaResource": self.default_lambda_resources(),
            "PowerValues": self.power_values()
        })


    @staticmethod
    def power_values():
        return '128,256,512,1024,1536,3008'

    @staticmethod
    def default_lambda_resources():
        return '*'