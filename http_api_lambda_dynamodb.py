import aws_cdk
import aws_cdk.aws_apigatewayv2_integrations_alpha
import aws_cdk.aws_apigatewayv2_alpha
import constructs
import well_architected
import well_architected_api
import well_architected_dynamodb_table
import well_architected_lambda
import well_architected_http_api
import well_architected_rest_api

class HttpApiLambdaDynamodb(well_architected.WellArchitectedStack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        partition_key='path',
        sort_key=None,
        time_to_live_attribute=None,
        lambda_function_name=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)
        self.error_topic = aws_cdk.aws_sns.Topic(
            self, 'SnsTopic',
            display_name=id
        )
        self.dynamodb_table = well_architected_dynamodb_table.DynamoDBTableConstruct(
            self, 'DynamoDbTable',
            error_topic=self.error_topic,
            partition_key=aws_cdk.aws_dynamodb.Attribute(
                name=partition_key,
                type=aws_cdk.aws_dynamodb.AttributeType.STRING,
            ),
            sort_key=sort_key,
            time_to_live_attribute=time_to_live_attribute,
        ).dynamodb_table
        self.lambda_function = well_architected_lambda.LambdaFunctionConstruct(
            self, 'LambdaFunction',
            error_topic=self.error_topic,
            function_name=lambda_function_name,
            environment_variables={
                'DYNAMODB_TABLE_NAME': self.dynamodb_table.table_name
            },
        ).lambda_function
        self.dynamodb_table.grant_read_write_data(self.lambda_function)

        self.http_api = well_architected_api.WellArchitectedApi(
            scope, 'HttpApi',
            error_topic=self.error_topic,
            api=aws_cdk.aws_apigatewayv2_alpha.HttpApi(
                self, 'LambdaFunctionIntegration',
                default_integration=aws_cdk.aws_apigatewayv2_integrations_alpha.HttpLambdaIntegration(
                    'LambdaFunction',
                    handler=self.lambda_function
                ),
            )
        ).api

        # self.rest_api = well_architected_rest_api.LambdaRestAPIGatewayConstruct(
        #     self, 'RestApiLambdaIntegration',
        #     error_topic=self.error_topic,
        #     lambda_function=self.lambda_function,
        # ).rest_api
        # web_application_firewall.WebApplicationFirewall(
        #     self, 'WebApplicationFirewall',
        #     target_arn=self.rest_api.resource_arn,
        # )