import constructs
import well_architected
import well_architected_constructs.api_lambda
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

        self.rest_api = well_architected_constructs.api_lambda.create_rest_api_lambda(
            self,
            lambda_function=self.lambda_function,
            error_topic=self.error_topic,
        )

        self.http_api = well_architected_constructs.api_lambda.create_http_api_lambda(
            self,
            error_topic=self.error_topic,
            lambda_function=self.lambda_function,
        )

        self.web_application_firewall = well_architected_constructs.web_application_firewall.WebApplicationFirewall(
            self, 'WebApplicationFirewall',
            error_topic=self.error_topic,
            target_arn= f"arn:aws:apigateway:region::/restapis/{self.rest_api.api_id}/stages/{self.rest_api.api.deployment_stage.stage_name}",
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