import cloudwatch

from aws_cdk.core import Stack, Construct, Duration
from aws_cdk.aws_lambda import Function, Code, Runtime
from aws_cdk.aws_sns import ITopic

# TODO
# separate alarms from widgets

class LambdaFunction(Stack):

    def __init__(self, scope: Construct, id: str,
        function_name=None, environment_variables=None, error_topic:ITopic=None,
        **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.error_topic = error_topic
        self.lambda_function = Function(
            self, "LambdaFunction",
            runtime=Runtime.PYTHON_3_8,
            handler=f'{function_name}.handler',
            code=Code.from_asset("lambda_functions"),
            timeout=Duration.seconds(60),
            environment=environment_variables,
        )


        self.lambda_function_cloudwatch_widgets = self.create_lambda_function_cloudwatch_widgets()

    def get_lambda_function_metric(self, metric_name):
        return self.lambda_function.metric(metric_name=metric_name, statistic="sum")

    def create_lambda_error_percentage_metric(self):
        # Gather the % of lambda invocations that error in past 5 mins
        return cloudwatch.create_cloudwatch_math_expression(
            expression="e / invocations * 100",
            label="% of invocations that errored, last 5 mins",
            using_metrics={
                "invocations": self.get_lambda_function_metric('Invocations'),
                "e": self.get_lambda_function_metric("Errors"),
            },
        )

    def create_lambda_error_percentage_widget(self):
        # 2% of Dynamo Lambda invocations erroring
        cloudwatch.create_cloudwatch_alarm(
            self, id="Dynamo Lambda 2% Error",
            metric=self.create_lambda_error_percentage_metric(),
            threshold=2,
            error_topic=self.error_topic,
        )
        return cloudwatch.create_cloudwatch_widget(
            title="Dynamo Lambda Error %",
            stacked=False,
            left=[self.create_lambda_error_percentage_metric()],
        )

    def create_lambda_duration_widget(self):
        # 1% of Lambda invocations taking longer than 1 second
        cloudwatch.create_cloudwatch_alarm(
            self, id="Dynamo Lambda p99 Long Duration (>1s)",
            metric=self.lambda_function.metric_duration(statistic="p99"),
            threshold=1000,
            error_topic=self.error_topic,
        )
        return cloudwatch.create_cloudwatch_widget(
            title="Dynamo Lambda Duration",
            left=[
                self.lambda_function.metric_duration(statistic=statistic)
                for statistic in ('p50', 'p90', 'p99')
            ],
        )

    def create_lambda_throttled_percentage_metric(self):
        # note: throttled requests are not counted in total num of invocations
        return cloudwatch.create_cloudwatch_math_expression(
            label="% of throttled requests, last 30 mins",
            expression="t / (invocations + t) * 100",
            using_metrics={
                "invocations": self.get_lambda_function_metric("Invocations"),
                "t": self.get_lambda_function_metric("Throttles"),
            },
        )

    def create_lambda_throttled_percentage_widget(self):
        # 2% of our lambda invocations are throttled
        cloudwatch.create_cloudwatch_alarm(
            self, id="Dynamo Lambda 2% Throttled",
            metric=self.create_lambda_throttled_percentage_metric(),
            threshold=2,
            error_topic=self.error_topic,
        )
        return cloudwatch.create_cloudwatch_widget(
            title="Dynamo Lambda Throttle %",
            left=[self.create_lambda_throttled_percentage_metric()],
            stacked=False,
        )

    def create_lambda_function_cloudwatch_widgets(self):
        return (
            self.create_lambda_error_percentage_widget(),
            self.create_lambda_duration_widget(),
            self.create_lambda_throttled_percentage_widget(),
        )