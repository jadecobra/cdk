import aws_cdk
import aws_cdk.aws_appsync_alpha
import constructs
import os


class SimpleGraphQlService(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        graphql_api = self.create_graphql_api()
        self.add_dynamodb_data_source_resolvers(
            graphql_api.add_dynamo_db_data_source(
                'DynamoDbDataSource',
                aws_cdk.aws_dynamodb.Table(
                    self, "DynamoDBTable",
                    partition_key=aws_cdk.aws_dynamodb.Attribute(
                        name="id",
                        type=aws_cdk.aws_dynamodb.AttributeType.STRING
                    )
                )
            )
        )
        self.add_get_customers_query_resolver_lambda(
            graphql_api.add_lambda_data_source(
                'LambdaDataSource',
                aws_cdk.aws_lambda.Function(
                    self, "LambdaFunction",
                    runtime=aws_cdk.aws_lambda.Runtime.PYTHON_3_9,
                    handler="loyalty.handler",
                    code=aws_cdk.aws_lambda.Code.from_asset("lambda_functions/loyalty"),
                )
            )
        )

        for logical_id, value in (
            ('Endpoint', graphql_api.graphql_url),
            ('API_Key', self.create_graphql_api_key(graphql_api.api_id).attr_api_key),
        ):
            aws_cdk.CfnOutput(self, logical_id, value=value)

    def create_graphql_api(self):
        return aws_cdk.aws_appsync_alpha.GraphqlApi(
            self, 'GraphQlApi',
            name="demoapi",
            log_config=aws_cdk.aws_appsync_alpha.LogConfig(
                field_log_level=aws_cdk.aws_appsync_alpha.FieldLogLevel.ALL
            ),
            schema=aws_cdk.aws_appsync_alpha.Schema.from_asset(
                f'{os.path.dirname(os.path.realpath(__file__))}/schema/schema.graphql'
            )
        )

    def create_graphql_api_key(self, api_id):
        return aws_cdk.aws_appsync.CfnApiKey(
            self, 'GraphQlApiKey',
            api_id=api_id
        )

    @staticmethod
    def create_query_resolver(
        data_source=None, field_name=None,
        request_mapping_template=None, response_mapping_template=None
    ):
        return data_source.create_resolver(
            type_name='Query',
            field_name=field_name,
            request_mapping_template=request_mapping_template,
            response_mapping_template=response_mapping_template,
        )

    def create_mutation_resolver(
        self, data_source=None, field_name=None,
        request_mapping_template=None, response_mapping_template=None
    ):
        return data_source.create_resolver(
            type_name='Mutation',
            field_name=field_name,
            request_mapping_template=request_mapping_template,
            response_mapping_template=aws_cdk.aws_appsync_alpha.MappingTemplate.dynamo_db_result_item(),
        )

    def add_get_customers_query_resolver_lambda(self, data_source):
        self.create_query_resolver(
            data_source=data_source,
            field_name='getLoyaltyLevel',
            request_mapping_template=aws_cdk.aws_appsync_alpha.MappingTemplate.lambda_request(),
            response_mapping_template=aws_cdk.aws_appsync_alpha.MappingTemplate.lambda_result(),
        )

    def add_get_customers_query_resolver_dynamodb(self, data_source):
        self.create_query_resolver(
            data_source=data_source,
            field_name='getCustomers',
            request_mapping_template=aws_cdk.aws_appsync_alpha.MappingTemplate.dynamo_db_scan_table(),
            response_mapping_template=aws_cdk.aws_appsync_alpha.MappingTemplate.dynamo_db_result_list(),
        )

    def add_get_customer_query_resolver(self, data_source):
        self.create_query_resolver(
            data_source=data_source,
            field_name='getCustomer',
            request_mapping_template=aws_cdk.aws_appsync_alpha.MappingTemplate.dynamo_db_get_item(
                'id', 'id'
            ),
            response_mapping_template=aws_cdk.aws_appsync_alpha.MappingTemplate.dynamo_db_result_item(),
        )

    def add_add_customer_mutation_resolver(self, data_source):
        self.create_mutation_resolver(
            data_source=data_source,
            field_name='addCustomer',
            request_mapping_template=aws_cdk.aws_appsync_alpha.MappingTemplate.dynamo_db_put_item(
                key=aws_cdk.aws_appsync_alpha.PrimaryKey.partition('id').auto(),
                values=aws_cdk.aws_appsync_alpha.Values.projecting('customer')
            ),
        )

    def add_save_customer_mutation_resolver(self, data_source):
        self.create_mutation_resolver(
            data_source=data_source,
            field_name='saveCustomer',
            request_mapping_template=aws_cdk.aws_appsync_alpha.MappingTemplate.dynamo_db_put_item(
                key=aws_cdk.aws_appsync_alpha.PrimaryKey.partition('id').is_('id'),
                values=aws_cdk.aws_appsync_alpha.Values.projecting('customer')
            ),
        )

    def add_save_customer_with_first_order_mutation_resolver(self, data_source):
        self.create_mutation_resolver(
            data_source=data_source,
            field_name='saveCustomerWithFirstOrder',
            request_mapping_template=aws_cdk.aws_appsync_alpha.MappingTemplate.dynamo_db_put_item(
                key=aws_cdk.aws_appsync_alpha.PrimaryKey.partition('order').auto().sort('customer').is_('customer.id'),
                values=aws_cdk.aws_appsync_alpha.Values.projecting('order').attribute('referral').is_('referral')
            ),
        )

    def add_remove_customer_mutation_resolver(self, data_source):
        self.create_mutation_resolver(
            data_source=data_source,
            field_name='removeCustomer',
            request_mapping_template=aws_cdk.aws_appsync_alpha.MappingTemplate.dynamo_db_delete_item('id', 'id'),
        )

    def add_dynamodb_data_source_resolvers(self, dynamodb_data_source):
        for method in (
            self.add_get_customers_query_resolver_dynamodb,
            self.add_get_customer_query_resolver,
            self.add_add_customer_mutation_resolver,
            self.add_save_customer_mutation_resolver,
            self.add_save_customer_with_first_order_mutation_resolver,
            self.add_remove_customer_mutation_resolver,
        ):
            method(dynamodb_data_source)