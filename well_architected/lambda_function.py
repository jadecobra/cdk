from aws_cdk.core import Construct, Duration, Stack
from aws_cdk.aws_lambda import Function, Code, Runtime, Tracing
from aws_cdk.aws_sns import ITopic
from well_architected import WellArchitectedFrameworkConstruct

class LambdaFunctionConstruct(WellArchitectedFrameworkConstruct):

    def __init__(self, scope: Construct, id: str,
        function_name=None, environment_variables=None, error_topic:ITopic=None,
        **kwargs) -> None:
        super().__init__(scope, id, error_topic=error_topic, **kwargs)
        self.lambda_function = Function(
            self, "LambdaFunction",
            runtime=Runtime.PYTHON_3_8,
            handler=f'{function_name}.handler',
            code=Code.from_asset("lambda_functions"),
            timeout=Duration.seconds(60),
            tracing=Tracing.ACTIVE,
            environment=environment_variables,
        )
        self.create_2_percent_error_alarm()
        self.create_long_duration_alarm()
        self.create_throttled_percentage_alarm()
        self.create_cloudwatch_dashboard(
            self.create_cloudwatch_widgets()
        )

    def get_lambda_function_metric(self, metric_name):
        return self.lambda_function.metric(metric_name=metric_name, statistic="sum")

    def create_lambda_error_percentage_metric(self):
        # Gather the % of lambda invocations that error in past 5 mins
        return self.create_cloudwatch_math_expression(
            expression="e / invocations * 100",
            label="% of invocations that errored, last 5 mins",
            using_metrics={
                "invocations": self.get_lambda_function_metric('Invocations'),
                "e": self.get_lambda_function_metric("Errors"),
            },
        )

    def create_lambda_throttled_percentage_metric(self):
        # note: throttled requests are not counted in total num of invocations
        return self.create_cloudwatch_math_expression(
            label="throttled requests % in last 30 mins",
            expression="t / (invocations + t) * 100",
            using_metrics={
                "invocations": self.get_lambda_function_metric("Invocations"),
                "t": self.get_lambda_function_metric("Throttles"),
            },
        )

    def create_2_percent_error_alarm(self):
        # 2% of Dynamo Lambda invocations erroring
        return self.create_cloudwatch_alarm(
            id="Lambda invocation Errors > 2%",
            metric=self.create_lambda_error_percentage_metric(),
            threshold=2,
        )

    def create_long_duration_alarm(self):
        # 1% of Lambda invocations taking longer than 1 second
        return self.create_cloudwatch_alarm(
            id="Lambda p99 Long Duration (>1s)",
            metric=self.lambda_function.metric_duration(statistic="p99"),
            threshold=1000,
        )

    def create_throttled_percentage_alarm(self):
        return self.create_cloudwatch_alarm(
            id="Lambda Throttled invocations >2%",
            metric=self.create_lambda_throttled_percentage_metric(),
            threshold=2,
        )

    def create_lambda_error_percentage_widget(self):
        return self.create_cloudwatch_widget(
            title="Lambda Error %",
            stacked=False,
            left=[self.create_lambda_error_percentage_metric()],
        )

    def create_lambda_duration_widget(self):
        return self.create_cloudwatch_widget(
            title="Lambda Duration",
            left=[
                self.lambda_function.metric_duration(statistic=statistic)
                for statistic in ('p50', 'p90', 'p99')
            ],
        )

    def create_lambda_throttled_percentage_widget(self):
        return self.create_cloudwatch_widget(
            title="Lambda Throttle %",
            left=[self.create_lambda_throttled_percentage_metric()],
            stacked=False,
        )

    def create_cloudwatch_widgets(self):
        return (
            self.create_lambda_error_percentage_widget(),
            self.create_lambda_duration_widget(),
            self.create_lambda_throttled_percentage_widget(),
        )

class LambdaFunctionStack(Stack):

    def __init__(self, scope: Construct, id: str,
        function_name=None, environment_variables=None, error_topic:ITopic=None,
        **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.lambda_function = create_python_lambda_function(
            self, function_name=function_name,
            environment_variables=environment_variables
        )

def create_python_lambda_function(stack, function_name=None, environment_variables=None):
    return LambdaFunctionConstruct(
        stack, function_name,
        function_name=function_name,
        environment_variables=environment_variables,
    ).lambda_function