from aws_cdk.core import Duration, Construct
from aws_cdk.aws_cloudwatch import Metric, Unit
from well_architected import WellArchitectedFramework


class ApiGatewayCloudWatch(Construct):

    def __init__(self, scope: Construct, id: str, api_id=None, error_topic=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.api_id = api_id
        self.error_topic = error_topic
        self.create_api_gateway_4xx_alarm()
        self.create_api_gateway_5xx_alarm()
        self.create_api_gateway_latency_alarm()
        self.create_cloudwatch_dashboard()

    def add_api_gateway_metric(self, metric_name: str = None, label: str = None,
            period=Duration.seconds(900), statistic: str = 'sum',
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
        # 4xx are user errors so a large volume indicates a problem
        return WellArchitectedFramework.create_cloudwatch_alarm(
            self, id="API Gateway 4XX Errors > 1%",
            metric=WellArchitectedFramework.create_cloudwatch_math_expression(
                expression="m1/m2*100",
                label="% API Gateway 4xx Errors",
                using_metrics={
                    "m1": self.add_api_gateway_metric(
                        metric_name='4XXError',
                        label='4XX Errors',
                    ),
                    "m2": self.add_api_gateway_metric(
                        metric_name='Count',
                        label='# Requests',
                    ),
                },
            ),
        )

    def create_api_gateway_5xx_alarm(self):
        # 5xx are internal server errors so we want 0 of these
        return WellArchitectedFramework.create_cloudwatch_alarm(
            self, id="API Gateway 5XX Errors > 0",
            metric=self.add_api_gateway_metric(
                metric_name="5XXError",
                label="5XX Errors",
                statistic="p99",
            ),
            threshold=0,
        )

    def create_api_gateway_latency_alarm(self):
        return WellArchitectedFramework.create_cloudwatch_alarm(
            self, id="API p99 latency alarm >= 1s",
            metric=self.add_api_gateway_metric(
                metric_name="Latency",
                label="API GW Latency",
                statistic="p99",
            ),
            threshold=1000,
        )

    def create_api_gateway_errors_widget(self):
        return WellArchitectedFramework.create_cloudwatch_widget(
            title="API GW Errors",
            left=[
                self.add_api_gateway_metric(
                    metric_name=metric_name,
                    label=label,
                ) for metric_name, label in (
                    ("4XXError", "4XX Errors"),
                    ("5XXError", "5XX Errors"),
                )
            ]
        )

    def create_api_gateway_latency_widget(self):
        return WellArchitectedFramework.create_cloudwatch_widget(
            title="API GW Latency",
            left=[
                self.add_api_gateway_metric(
                    metric_name="Latency",
                    label=label,
                    statistic=statistic,
                ) for label, statistic in (
                    ("API Latency p50", "p50"),
                    ("API Latency p90", "p90"),
                    ("API Latency p99", "p99"),
                )
            ]
        )

    def create_api_gateway_number_of_requests_widget(self):
        return WellArchitectedFramework.create_cloudwatch_widget(
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

    def create_cloudwatch_dashboard(self):
        return WellArchitectedFramework.create_cloudwatch_dashboard(
            self, widgets=self.create_cloudwatch_widgets()
        )