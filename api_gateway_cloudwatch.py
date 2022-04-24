import aws_cdk
import constructs

from aws_cdk.aws_cloudwatch import Metric, Unit
from well_architected import WellArchitectedFrameworkConstruct

class ApiGatewayCloudWatch(WellArchitectedFrameworkConstruct):

    def __init__(self,
        scope: constructs.Construct, id: str, api_id=None,
        error_topic=None, **kwargs
    ) -> None:
        super().__init__(
            scope, id, error_topic=error_topic, **kwargs
        )
        self.api_id = api_id
        self.create_api_gateway_4xx_alarm()
        self.create_api_gateway_5xx_alarm()
        self.create_api_gateway_latency_alarm()
        self.create_cloudwatch_dashboard(self.create_cloudwatch_widgets())

    def add_api_gateway_metric(self, metric_name: str = None, label: str = None,
            period=aws_cdk.Duration.seconds(900), statistic: str = 'sum',
        ):
        return Metric(
            metric_name=metric_name,
            namespace="AWS/ApiGateway",
            dimensions_map={"ApiId": self.api_id},
            unit=Unit.COUNT,
            label=label,
            statistic=statistic,
            period=period,
        )

    def create_api_gateway_4xx_alarm(self):
        return self.create_cloudwatch_alarm(
            id="ApiGateway4XXErrorsGreaterThan1Percent",
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
            id="APIGateway5XXErrorsGreaterThan0",
            metric=self.add_api_gateway_metric(
                metric_name="5XXError",
                label="api_gateway_5XX_errors",
                statistic="p99",
            ),
            threshold=0,
        )

    def create_api_gateway_latency_alarm(self):
        return self.create_cloudwatch_alarm(
            id="ApiGatewayP99LatencyGreaterThan1s",
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