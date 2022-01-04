from aws_cdk.core import Duration
from aws_cdk.aws_cloudwatch import (
    MathExpression, GraphWidget, Alarm, TreatMissingData, Dashboard
)
from aws_cdk.aws_cloudwatch_actions import SnsAction

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

def create_cloudwatch_widget(title=None, stacked=True, left=None):
    return GraphWidget(
        title=title, width=8, stacked=stacked, left=left
    )

def create_cloudwatch_alarm(stack, id=None, metric=None, threshold=1, error_topic=None):
    return Alarm(
        stack,
        id=id,
        metric=metric,
        threshold=threshold,
        evaluation_periods=6,
        datapoints_to_alarm=1,
        treat_missing_data=TreatMissingData.NOT_BREACHING,
    ).add_alarm_action(
        SnsAction(error_topic)
    )

def create_cloudwatch_dashboard(stack, widgets=None):
    return Dashboard(
        stack, "CloudWatchDashBoard",
        widgets=[
            [widget] for widget in widgets
        ]
    )