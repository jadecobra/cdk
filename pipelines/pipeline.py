import aws_cdk.aws_codepipeline as codepipeline

# how to construct an empty pipeline - $1/month for KMS
pipeline = codepipeline.Pipeline(self, 'Pipeline')
pipeline = codepipeline.Pipeline(
    self, 'Pipeline',
    pipeline_name='Pipeline',
)

# how to disable cross_account deployments
pipeline = codepipeline.Pipeline(
    self, 'Pipeline',
    cross_account_keys=False,
)

# how to enable key rotation for KMS keys - $2/month
pipeline = codepipeline.Pipeline(
    self, 'Pipeline',
    enable_key_rotation=True,
)

# how to provide a stage when creating a pipeline
pipeline = codepipeline.Pipeline(
    self, 'Pipeline',
    stages=[
        codepipeline.StageProps(
            stage_name='Source',
            actions=[]
        )
    ]
)

# how to append a stage to an existing pipeline:
pipeline = codepipeline.Pipeline(
    self, 'Pipeline',
)
source_stage = pipeline.add_stage(
    stage_name='Source',
    actions=[]
)

# how to insert a stage at an arbitrary point in the Pipeline
pipeline = codepipeline.Pipeline(
    self, 'Pipeline',
)
arbitrary_stage = pipeline.add_stage(
    stage_name='Arbitrary',
    placement=codepipeline.StagePlacement(
        right_before=next_stage
    )
)
arbitrary_stage = pipeline.add_stage(
    stage_name='Arbitrary',
    placement=codepipeline.StagePlacement(
        just_after=previous_stage
    )
)