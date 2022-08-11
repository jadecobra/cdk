import constructs
import regular_constructs.autoscaling_ecs
import well_architected


class AutoscalingEcsCluster(well_architected.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        regular_constructs.autoscaling_ecs.AutoscalingEcsCluster(
            self, 'AutoscalingEcs',
        )