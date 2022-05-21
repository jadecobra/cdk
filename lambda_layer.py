import aws_cdk
import constructs

class LambdaLayer(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, layer_name=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.lambda_layer = aws_cdk.aws_lambda.LayerVersion(
            self, "LambdaLayer",
            code=aws_cdk.aws_lambda.Code.from_asset(f"lambda_layers/{layer_name}"),
            description=f"{layer_name} Lambda Layer",
        )