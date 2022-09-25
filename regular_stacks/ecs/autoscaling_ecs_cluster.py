import constructs
import well_architected_stacks

from . import autoscaling_ecs



class AutoscalingEcsCluster(well_architected_stacks.well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        autoscaling_ecs.AutoscalingEcsClusterConstruct(
            self, 'AutoscalingEcs',
        )