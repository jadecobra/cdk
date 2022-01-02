from aws_cdk.core import Duration
from aws_cdk.aws_cloudwatch import MathExpression

def five_minutes():
    return Duration.minutes(5)

def create_cloudwatch_math_expression(expression=None, label=None, using_metrics=None):
    return MathExpression(
        expression=expression,
        label=label,
        using_metrics=using_metrics,
        period=five_minutes(),
    )

def cloudwatch_math_sum(label=None, m1=None, m2=None):
    return create_cloudwatch_math_expression(
        label=label,
        expression="m1 + m2",
        using_metrics={"m1": m1, "m2": m2},
    )
