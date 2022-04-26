# import aws_cdk
# import constructs
# import well_architected_api
# import aws_cdk.aws_apigatewayv2_alpha
# import aws_cdk.aws_apigatewayv2_integrations_alpha
# import well_architected


# class LambdaHttpApiGateway(well_architected.WellArchitectedStack):

#     def __init__(
#         self, scope: constructs.Construct, id: str,
#         lambda_function: aws_cdk.aws_lambda.Function,
#         error_topic=None,
#         **kwargs
#     ) -> None:
#         super().__init__(scope, id, **kwargs)

#         self.http_api = HttpApi(
#             self, id,
#             default_integration=aws_cdk.aws_apigatewayv2_integrations_alpha.HttpLambdaIntegration(
#                 'HttpApiLambdaIntegration',
#                 handler=lambda_function
#             )
#         ).http_api
