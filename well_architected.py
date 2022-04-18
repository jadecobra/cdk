import aws_cdk
import constructs

from aws_cdk import Stack, Duration
from aws_cdk.aws_cloudwatch import Dashboard, GraphWidget, MathExpression, Alarm, TreatMissingData

from aws_cdk.aws_cloudwatch_actions import SnsAction
from aws_cdk.aws_sns import Topic


class WellArchitectedFrameworkConstruct(constructs.Construct):

    def __init__(self, scope: constructs.Construct, id: str, error_topic=None, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.error_topic = error_topic if error_topic else self.create_error_topic()

    def create_error_topic(self):
        return Topic(
            self, "ErrorTopic",
            display_name="ErrorTopic",
        )

    @staticmethod
    def create_cloudwatch_math_expression(expression=None, label=None, using_metrics=None):
        return MathExpression(
            expression=expression,
            label=label,
            using_metrics=using_metrics,
            period=Duration.minutes(5),
        )

    def cloudwatch_math_sum(self, label=None, m1=None, m2=None):
        return self.create_cloudwatch_math_expression(
            label=label,
            expression="m1 + m2",
            using_metrics={"m1": m1, "m2": m2},
        )

    @staticmethod
    def create_cloudwatch_widget(title=None, stacked=True, left=None):
        return GraphWidget(
            title=title, width=8, stacked=stacked, left=left
        )

    def create_cloudwatch_alarm(self, id=None, metric=None, threshold=1):
        return Alarm(
            self,
            id=id,
            metric=metric,
            threshold=threshold,
            evaluation_periods=6,
            datapoints_to_alarm=1,
            treat_missing_data=TreatMissingData.NOT_BREACHING,
        ).add_alarm_action(
            SnsAction(self.error_topic)
        )

    def create_cloudwatch_dashboard(self, widgets):
        return Dashboard(
            self, "CloudWatchDashBoard",
            widgets=[
                [widget] for widget in widgets
            ]
        )