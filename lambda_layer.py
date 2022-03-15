from aws_cdk.core import Construct, Stack
from aws_cdk.aws_lambda import LayerVersion, Code

class LambdaLayer(Stack):

    def __init__(self, scope: Construct, id: str, layer_name=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.lambda_layer = LayerVersion(
            self, "LambdaLayer",
            code=Code.from_asset(f"lambda_layers/{layer_name}"),
            description=f"{layer_name} Lambda Layer",
        )