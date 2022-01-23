import aws_cdk.pipelines as pipelines

# approval steps
preprod = MyApplicationStage(self, 'PreProd')
prod = MyApplicationStage(self, 'Prod')

pipeline.add_stage(
    preprod,
    post=[
        pipelines.ShellStep(
            'ValidateEndpoint',
            commands=['curl -Ssf http://my.webservice.com/']
        )
    ]
)
pipeline.add_stage(
    pre=[
        pipelines.ManualApprovalStep('PromoteToProd')
    ]
)

# how to specify steps at the stack level
class MyStacksSTage(pipelines.Stage):

    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)
        self.stack1 = Stack(self, 'stack1')
        self.stack2 = Stack(self, 'stack2')

prod = MyStacksStage(self, 'Prod')
pipeline.add_stage(
    prod,
    stack_steps=[
        pipelines.StackSteps(
            stack=prod.stack1,
            pre=[pipelines.ManualApprovalStep('Pre-Stack Check')],
            change_set=[pipelines.ManualApprovalStep('ChangeSet Approval')],
            post=[pipelines.ManualApprovalStep('Post-Deploy Check')]
        ),
        pipelines.StackSteps(
            stack=prod.stack2,
            post=[pipelines.ManualApprovalStep('Post-Deploy Check')]
        )
    ]
)

# how to specify step dependencies
# steps execute in parallel by default until you add a dependency
step_1 = pipelines.ManualApprovalStep('A')
step_2 = pipelines.ManualApprovalStep('B')
step_2.add_step_dependency(step_1)

# how to execute steps in sequence
pipelines.Step.sequence([
    pipelines.ManualApprovalStep('A'),
    pipelines.ManualApprovalStep('B'),
    pipelines.ManualApprovalStep('C'),
    pipelines.ManualApprovalStep('N'),
])

# how to use cloudformation stack outputs in approvals
class MyOutputStage(pipelines.Stage):

    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)
        self.load_balancer_address = CfnOutput(self, 'Output', value='value')

load_balanced_app = MyOutputStage(self, 'LoadBalancedApp')
pipeline.add_stage(
    load_balanced_app,
    post=[
        pipelines.ShellStep(
            'HitEndpoint',
            env_from_cfn_outputs={
                'URL': load_balanced_app.load_balancer_address
            },
            commands=['curl -Ssf $URL']
        )
    ]
)

# how to run scripts compiled during the synth step
# synth: pipelines.ShellStep
stage = MyApplicationStage(self, 'MyApplication')
pipeline = pipelines.CodePipeline(self, 'Pipeline', synth=synth)
pipeline.add_stage(
    stage,
    post=[
        pipelines.ShellStep(
            'Approve',
            input=synth.add_output_directory('integ')
            commands=['cd integ && ./run.sh']
        )
    ]
)