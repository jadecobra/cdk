import aws_cdk
import aws_cdk.aws_lambda
import aws_cdk.aws_dynamodb
import aws_cdk.aws_appsync
import constructs
import os


class SimpleGraphQlService(aws_cdk.core.Stack):



    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a new AppSync GraphQL API
        api = aws_cdk.aws_appsync.GraphqlApi(
            self, 'Api',
            name="demoapi",
            log_config=aws_cdk.aws_appsync.LogConfig(
                field_log_level=aws_cdk.aws_appsync.FieldLogLevel.ALL
            ),
            schema=aws_cdk.aws_appsync.Schema.from_asset(
                os.path.dirname(os.path.realpath(__file__)) + "/schema/schema.graphql"
            )
        )

        api_key = aws_cdk.aws_appsync.CfnApiKey(
            self, 'the-simple-graphql-service-api-key',
            api_id=api.api_id
        )

        customer_data_table = self.create_dynamodb_table()
        loyalty_lambda = self.create_lambda_function()
        customer_data_source = api.add_dynamo_db_data_source('Customer', customer_data_table)
        loyalty_data_source = api.add_lambda_data_source('Loyalty', loyalty_lambda)

        self.add_get_customers_query_resolver_dynamodb(customer_data_source)
        self.add_get_customer_query_resolver(customer_data_source)
        self.add_add_customer_mutation_resolver(customer_data_source)
        self.add_save_customer_mutation_resolver(customer_data_source)
        self.add_save_customer_with_first_order_mutation_resolver(customer_data_source)
        self.add_remove_customer_mutation_resolver(customer_data_source)
        self.add_get_customers_query_resolver_lambda(loyalty_data_source)
        # Query Resolver to get all Customers
        # loyalty_data_source.create_resolver(
        #     type_name='Query',
        #     field_name='getLoyaltyLevel',
        #     request_mapping_template=aws_cdk.aws_appsync.MappingTemplate.lambda_request(),
        #     response_mapping_template=aws_cdk.aws_appsync.MappingTemplate.lambda_result(),
        # )

        for logical_id, value in (
            ('Endpoint', api.graphql_url),
            ('API_Key', api_key.attr_api_key),
        ):
            aws_cdk.core.CfnOutput(self, logical_id, value=value)


    def create_dynamodb_table(self):
        return aws_cdk.aws_dynamodb.Table(
            self, "CustomerTable",
            partition_key=aws_cdk.aws_dynamodb.Attribute(
                name="id",
                type=aws_cdk.aws_dynamodb.AttributeType.STRING
            )
        )

    def create_lambda_function(self):
        return aws_cdk.aws_lambda.Function(self, "LoyaltyLambdaHandler",
            runtime=aws_cdk.aws_lambda.Runtime.NODEJS_12_X,
            handler="loyalty.handler",
            code=aws_cdk.aws_lambda.Code.from_asset("lambda_functions"),
        )

    @staticmethod
    def add_get_customers_query_resolver_lambda(data_source):
        data_source.create_resolver(
            type_name='Query',
            field_name='getLoyaltyLevel',
            request_mapping_template=aws_cdk.aws_appsync.MappingTemplate.lambda_request(),
            response_mapping_template=aws_cdk.aws_appsync.MappingTemplate.lambda_result(),
        )

    @staticmethod
    def add_get_customers_query_resolver_dynamodb(data_source):
        data_source.create_resolver(
            type_name='Query',
            field_name='getCustomers',
            request_mapping_template=aws_cdk.aws_appsync.MappingTemplate.dynamo_db_scan_table(),
            response_mapping_template=aws_cdk.aws_appsync.MappingTemplate.dynamo_db_result_list(),
        )

    @staticmethod
    def add_get_customer_query_resolver(data_source):
        # Query Resolver to get an individual Customer by their id
        data_source.create_resolver(
            type_name='Query',
            field_name='getCustomer',
            request_mapping_template=aws_cdk.aws_appsync.MappingTemplate.dynamo_db_get_item(
                'id', 'id'
            ),
            response_mapping_template=aws_cdk.aws_appsync.MappingTemplate.dynamo_db_result_item(),
        )

    @staticmethod
    def add_add_customer_mutation_resolver(data_source):
        data_source.create_resolver(
            type_name='Mutation',
            field_name='addCustomer',
            request_mapping_template=aws_cdk.aws_appsync.MappingTemplate.dynamo_db_put_item(
                key=aws_cdk.aws_appsync.PrimaryKey.partition('id').auto(),
                values=aws_cdk.aws_appsync.Values.projecting('customer')
            ),
            response_mapping_template=aws_cdk.aws_appsync.MappingTemplate.dynamo_db_result_item()
        )

    @staticmethod
    def add_save_customer_mutation_resolver(data_source):
        data_source.create_resolver(
            type_name='Mutation',
            field_name='saveCustomer',
            request_mapping_template=aws_cdk.aws_appsync.MappingTemplate.dynamo_db_put_item(
                key=aws_cdk.aws_appsync.PrimaryKey.partition('id').is_('id'),
                values=aws_cdk.aws_appsync.Values.projecting('customer')
            ),
            response_mapping_template=aws_cdk.aws_appsync.MappingTemplate.dynamo_db_result_item()
        )

    @staticmethod
    def add_save_customer_with_first_order_mutation_resolver(data_source):
        data_source.create_resolver(
            type_name='Mutation',
            field_name='saveCustomerWithFirstOrder',
            request_mapping_template=aws_cdk.aws_appsync.MappingTemplate.dynamo_db_put_item(
                key=aws_cdk.aws_appsync.PrimaryKey.partition('order').auto().sort('customer').is_('customer.id'),
                values=aws_cdk.aws_appsync.Values.projecting('order').attribute('referral').is_('referral')
            ),
            response_mapping_template=aws_cdk.aws_appsync.MappingTemplate.dynamo_db_result_item()
        )

    @staticmethod
    def add_remove_customer_mutation_resolver(data_source):
        data_source.create_resolver(
            type_name='Mutation',
            field_name='removeCustomer',
            request_mapping_template=aws_cdk.aws_appsync.MappingTemplate.dynamo_db_delete_item('id', 'id'),
            response_mapping_template=aws_cdk.aws_appsync.MappingTemplate.dynamo_db_result_item(),
        )
