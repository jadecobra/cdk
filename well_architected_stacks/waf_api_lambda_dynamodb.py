import aws_cdk
import aws_cdk.aws_apigatewayv2_integrations_alpha
import aws_cdk.aws_apigatewayv2_alpha
import constructs
import well_architected
import well_architected_constructs.api
import well_architected_constructs.dynamodb_table
import well_architected_constructs.lambda_function
import well_architected_constructs.web_application_firewall


class WafApiLambdaDynamodb(well_architected.Stack):

    @staticmethod
    def camel_to_snake(text):
        return ''.join([
            '_'+character.lower()
            if character.isupper()
            else character
            for character in text
        ]).lstrip('_')

    def __init__(
        self, scope: constructs.Construct, id: str,
        partition_key='path',
        sort_key=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)
        self.name = self.camel_to_snake(id)

        self.dynamodb_table = self.create_dynamodb_table(
            name=self.name,
            partition_key=partition_key,
            sort_key=sort_key,
            error_topic=self.error_topic,
        )
        self.lambda_function = self.create_lambda_function(
            error_topic=self.error_topic,
            name=self.name,
        )
        self.dynamodb_table.grant_read_write_data(self.lambda_function)

        self.rest_api = self.create_rest_api(
            lambda_function=self.lambda_function,
            error_topic=self.error_topic,
        )

        self.web_application_firewall = well_architected_constructs.web_application_firewall.WebApplicationFirewall(
            self, 'WebApplicationFirewall',
            error_topic=self.error_topic,
            target_arn= f"arn:aws:apigateway:region::/restapis/{self.rest_api.api_id}/stages/{self.rest_api.api.deployment_stage.stage_name}",
        )
        self.http_api = self.create_http_api(
            error_topic=self.error_topic,
            name=self.name,
            lambda_function=self.lambda_function,
            api_gateway_service_role=self.rest_api.api_gateway_service_role
        )

    def create_dynamodb_table(self, error_topic=None, name=None, partition_key=None, sort_key=None):
        return well_architected_constructs.dynamodb_table.DynamoDBTableConstruct(
            self, 'DynamoDbTable',
            table_name=name,
            error_topic=error_topic,
            partition_key=partition_key,
            sort_key=sort_key, # refactor this
        ).dynamodb_table

    def create_lambda_function(self, error_topic=None, name=None):
        return well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, 'LambdaFunction',
            error_topic=error_topic,
            function_name=name,
            environment_variables={
                'DYNAMODB_TABLE_NAME': name
            },
        ).lambda_function

    def create_http_api(
        self, name=None, lambda_function=None,
        error_topic=None, api_gateway_service_role=None,
        ):
        return well_architected_constructs.api.Api(
            self, 'HttpApiGateway',
            error_topic=error_topic,
            api_gateway_service_role=api_gateway_service_role,
            api=aws_cdk.aws_apigatewayv2_alpha.HttpApi(
                self, 'HttpApi',
                api_name=name,
                default_integration=aws_cdk.aws_apigatewayv2_integrations_alpha.HttpLambdaIntegration(
                    'LambdaFunction',
                    handler=lambda_function
                ),
            )
        )

    def create_rest_api(self, lambda_function=None, error_topic=None):
        return well_architected_constructs.api.Api(
            self, 'RestApiGateway',
            error_topic=error_topic,
            api=aws_cdk.aws_apigateway.LambdaRestApi(
                self, 'RestApi',
                handler=lambda_function,
            )
        )