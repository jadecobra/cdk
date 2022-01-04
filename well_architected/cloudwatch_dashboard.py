from aws_cdk.core import Stack, Construct
from aws_cdk.aws_cloudwatch import Dashboard

class CloudWatchDashboard(Stack):
    '''Create a CloudWatch Dashboard with the given widgets'''

    def __init__(
        self, scope: Construct, id: str,
        *widgets,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        Dashboard(
            self, "CloudWatchDashBoard",
            widgets=[[*widget] for widget in widgets]
        )