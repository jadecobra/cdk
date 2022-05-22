import aws_cdk
import aws_cdk.aws_apigatewayv2_alpha
import constructs
import well_architected

class WellArchitectedRestApiSns(well_architected.WellArchitectedStack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

    @staticmethod
    def create_schema(title=None, properties=None):
        return aws_cdk.aws_apigateway.JsonSchema(
            schema=aws_cdk.aws_apigateway.JsonSchemaVersion.DRAFT4,
            title=title,
            type=aws_cdk.aws_apigateway.JsonSchemaType.OBJECT,
            properties=properties
        )

    @staticmethod
    def string_schema_type():
        return aws_cdk.aws_apigateway.JsonSchema(
            type=aws_cdk.aws_apigateway.JsonSchemaType.STRING
        )

    def create_response_model(
        self, rest_api=None, model_name=None, properties=None
    ):
        property_keys = ['message']
        property_keys.append(properties) if properties else None
        return rest_api.add_model(
            model_name,
            content_type='application/json',
            model_name=model_name,
            schema=self.create_schema(
                title=model_name,
                properties={key: self.string_schema_type() for key in property_keys},
            )
        )

    @staticmethod
    def create_json_template(template):
        return {'application/json': template}

    @staticmethod
    def create_response_parameters(content_type=True, allow_origin=True, allow_credentials=True):
        return {
            'method.response.header.Content-Type': content_type,
            'method.response.header.Access-Control-Allow-Origin': allow_origin,
            'method.response.header.Access-Control-Allow-Credentials': allow_credentials,
        }

    def create_method_response(self, status_code=None, response_model=None):
        return aws_cdk.aws_apigateway.MethodResponse(
            status_code=str(status_code),
            response_parameters=self.create_response_parameters(),
            response_models=self.create_json_template(response_model)
        )

    def create_method_responses(self, rest_api):
        return [
            self.create_method_response(
                status_code=200,
                response_model=self.create_response_model(
                    rest_api=rest_api,
                    model_name='pollResponse',
                )
            ),
            self.create_method_response(
                status_code=400,
                response_model=self.create_response_model(
                    rest_api=rest_api,
                    model_name='errorResponse',
                    properties='state',
                )
            )
        ]

    @staticmethod
    def get_stage_options():
        return aws_cdk.aws_apigateway.StageOptions(
            metrics_enabled=True,
            logging_level=aws_cdk.aws_apigateway.MethodLoggingLevel.INFO,
            data_trace_enabled=True,
            stage_name='prod'
        )

class WellArchitectedApi(well_architected.WellArchitectedConstruct):

    def __init__(
        self,scope: constructs.Construct, id: str, api_id=None,
        error_topic=None,
        api=None,
        **kwargs
    ) -> None:
        super().__init__(
            scope, id,
            error_topic=error_topic,
            **kwargs
        )
        self.api = api
        self.api_id = self.get_api_id(api)
        self.create_api_gateway_4xx_alarm()
        self.create_api_gateway_5xx_alarm()
        self.create_api_gateway_latency_alarm()
        self.create_cloudwatch_dashboard(self.create_cloudwatch_widgets())
        aws_cdk.CfnOutput(self, f'{id} URL', value=api.url)

    def get_api_id(self, api):
        try:
            return api.api_id
        except AttributeError:
            return api.rest_api_id

    def add_api_gateway_metric(self, metric_name: str = None, label: str = None,
            period=aws_cdk.Duration.seconds(900), statistic: str = 'sum',
        ):
        return aws_cdk.aws_cloudwatch.Metric(
            metric_name=metric_name,
            namespace="AWS/ApiGateway",
            dimensions_map={"ApiId": self.api_id},
            unit=aws_cdk.aws_cloudwatch.Unit.COUNT,
            label=label,
            statistic=statistic,
            period=period,
        )

    def create_api_gateway_4xx_alarm(self):
        return self.create_cloudwatch_alarm(
            id="4XXErrorsGreaterThanOnePercent",
            metric=self.create_cloudwatch_math_expression(
                expression="m1 / m2 * 100",
                label="api_gateway_4XX_errors_percentage",
                using_metrics={
                    "m1": self.add_api_gateway_metric(
                        metric_name='4XXError',
                        label='4XX_errors',
                    ),
                    "m2": self.add_api_gateway_metric(
                        metric_name='Count',
                        label='number_of_requests',
                    ),
                },
            ),
        )

    def create_api_gateway_5xx_alarm(self):
        return self.create_cloudwatch_alarm(
            id="5XXErrorsGreaterThanZero",
            metric=self.add_api_gateway_metric(
                metric_name="5XXError",
                label="api_gateway_5XX_errors",
                statistic="p99",
            ),
            threshold=0,
        )

    def create_api_gateway_latency_alarm(self):
        return self.create_cloudwatch_alarm(
            id="P99LatencyGreaterThanOneSecond",
            metric=self.add_api_gateway_metric(
                metric_name="Latency",
                label="api_gateway_latency",
                statistic="p99",
            ),
            threshold=1000,
        )

    @staticmethod
    def percentile_statistics():
        return ("p50", "p90", "p99",)

    @staticmethod
    def metric_names():
        return (f'{code}XXError' for code in ('4', '5'))

    def create_api_gateway_errors_widget(self):
        return self.create_cloudwatch_widget(
            title="api_gateway_errors",
            left=[
                self.add_api_gateway_metric(
                    metric_name=metric_name,
                    label=f'api_gateway_{metric_name}s',
                ) for metric_name in self.metric_names()
            ]
        )

    def create_api_gateway_latency_widget(self):
        return self.create_cloudwatch_widget(
            title="api_gateway_latency",
            left=[
                self.add_api_gateway_metric(
                    metric_name="Latency",
                    label=f'api_gateway_latency_{statistic}',
                    statistic=statistic,
                ) for statistic in self.percentile_statistics()
            ]
        )

    def create_api_gateway_number_of_requests_widget(self):
        return self.create_cloudwatch_widget(
            title="Requests",
            stacked=False,
            left=[
                self.add_api_gateway_metric(
                    metric_name="Count",
                    label="# Requests",
                )
            ]
        )

    def create_cloudwatch_widgets(self):
        return (
            self.create_api_gateway_number_of_requests_widget(),
            self.create_api_gateway_latency_widget(),
            self.create_api_gateway_errors_widget(),
        )