from aws_cdk.core import Construct, Duration, Stack
from aws_cdk.aws_lambda import Function, Code, Runtime, Tracing, LayerVersion
from aws_cdk.aws_sns import ITopic
from well_architected import WellArchitectedFrameworkConstruct
import utilities

class LambdaFunctionConstruct(WellArchitectedFrameworkConstruct):

    def __init__(self, scope: Construct, id: str,
        function_name=None, handler_name=None,
        environment_variables=None,
        error_topic:ITopic=None, layers:list[str]=None,
        concurrent_executions=None,
        duration=60, vpc=None,
        **kwargs) -> None:
        super().__init__(scope, id, error_topic=error_topic, **kwargs)
        handler_name = 'handler' if handler_name is None else handler_name
        self.lambda_function = Function(
            self, id, # can we use id as function_name
            runtime=Runtime.PYTHON_3_9,
            handler=f'{function_name}.{handler_name}',
            code=Code.from_asset(f"lambda_functions/{function_name}"),
            timeout=Duration.seconds(duration),
            tracing=Tracing.ACTIVE,
            layers=self.create_layers(layers),
            vpc=vpc,
            reserved_concurrent_executions=concurrent_executions,
            environment=environment_variables,
        )
        self.create_2_percent_error_alarm()
        self.create_long_duration_alarm()
        self.create_throttled_percentage_alarm()
        self.create_cloudwatch_dashboard(
            self.create_cloudwatch_widgets()
        )

    def create_layer(self, layer):
        return LayerVersion(
            self, f'{layer}LambdaLayer',
            code=Code.from_asset(f"lambda_layers/{layer}"),
            description=f"AWS XRay SDK Lambda Layer"
        )

    def create_layers(self, layers):
        result = [self.create_layer('aws-xray-sdk')]
        try:
            for layer in layers:
                result.append(self.create_layer(layer))
        except TypeError:
            'No additional layers specified'
        return result

    def get_lambda_function_metric(self, metric_name):
        return self.lambda_function.metric(metric_name=metric_name, statistic="sum")

    def create_lambda_error_percentage_metric(self):
        return self.create_cloudwatch_math_expression(
            expression="(errors / invocations) * 100",
            label="% of invocations that errored, last 5 mins",
            using_metrics={
                "invocations": self.get_lambda_function_metric('Invocations'),
                "errors": self.get_lambda_function_metric("Errors"),
            },
        )

    def create_lambda_throttled_percentage_metric(self):
        # note: throttled requests are not counted in total number of invocations
        return self.create_cloudwatch_math_expression(
            label="throttled requests % in last 30 mins",
            expression="(throttles * 100) / (invocations + throttles)",
            using_metrics={
                "invocations": self.get_lambda_function_metric("Invocations"),
                "throttles": self.get_lambda_function_metric("Throttles"),
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
        handler_name=None,
        **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.lambda_function = create_python_lambda_function(
            self, function_name=function_name,
            environment_variables=environment_variables,
            error_topic=error_topic,
            handler_name=handler_name,
        )

def create_python_lambda_function(
        stack,
        function_name=None, handler_name=None,
        environment_variables=None,
        duration=60, error_topic=None, vpc=None,
        concurrent_executions=None,
    ):
    return LambdaFunctionConstruct(
        stack, function_name,
        function_name=function_name,
        handler_name=handler_name,
        environment_variables=environment_variables,
        duration=duration,
        error_topic=error_topic,
        vpc=vpc,
        concurrent_executions=concurrent_executions,
    ).lambda_function