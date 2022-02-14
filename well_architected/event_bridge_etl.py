from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_event_sources,
    aws_dynamodb as dynamo_db,
    aws_s3 as s3,
    aws_s3_notifications as s3_notifications,
    aws_sqs as sqs,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
    aws_events as events,
    aws_events_targets as event_bridge_targets,
    core as cdk
)
import json
import dynamodb_table


class EventbridgeEtl(cdk.Stack):

    # If left unchecked this pattern could "fan out" on the transform and load
    # lambdas to the point that it consumes all resources on the account. This is
    # why we are limiting concurrency to 2 on all 3 lambdas. Feel free to raise this.
    lambda_throttle_size = 2

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.upload_bucket = s3.Bucket(self, "LandingBucket")

        self.transformed_data = self.create_dynamodb_table()
        self.upload_queue = self.create_sqs_queue()
        self.create_s3_sqs_notification(
            bucket=self.upload_bucket, sqs_queue=self.upload_queue
        )
        self.event_bridge_put_policy = self.create_event_bridge_iam_policy()

        ####
        # Fargate ECS Task Creation to pull data from S3
        #
        # Fargate is used here because if you had a seriously large file,
        # you could stream the data to fargate for as long as needed before
        # putting the data onto eventbridge or up the memory/storage to
        # download the whole file. Lambda has limitations on runtime and
        # memory/storage
        ####
        self.vpc = ec2.Vpc(self, "Vpc", max_azs=2)
        self.subnet_ids = [subnet.subnet_id for subnet in self.vpc.private_subnets]

        self.logging = ecs.AwsLogDriver(
            stream_prefix='TheEventBridgeETL',
            log_retention=logs.RetentionDays.ONE_WEEK
        )

        self.ecs_cluster = ecs.Cluster(self, 'Ec2Cluster', vpc=self.vpc)

        self.task_definition = ecs.TaskDefinition(
            self, 'FargateTaskDefinition',
            memory_mib="512",
            cpu="256",
            compatibility=ecs.Compatibility.FARGATE
        )
        self.task_definition.add_to_task_role_policy(self.event_bridge_put_policy)
        self.upload_bucket.grant_read(self.task_definition.task_role)

        self.extraction_task = self.task_definition.add_container(
            'AppContainer',
            image=ecs.ContainerImage.from_asset('containers/s3DataExtractionTask'),
            logging=self.logging,
            environment={
                'S3_BUCKET_NAME': self.upload_bucket.bucket_name,
                'S3_OBJECT_KEY': ''
            }
        )

        ####
        # Lambdas
        #
        # These are used for 4 phases:
        #
        # Extract    - kicks of ecs fargate task to download data and splinter to eventbridge events
        # Transform  - takes the two comma separated strings and produces a json object
        # Load       - inserts the data into dynamodb
        # Observe    - This is a lambda that subscribes to all events and logs them centrally
        ####

        ####
        # Extract
        # defines an AWS Lambda resource to trigger our fargate ecs task
        ####
        extractor = _lambda.Function(
            self, "extractLambdaHandler",
            runtime=_lambda.Runtime.NODEJS_12_X,
            handler="s3SqsEventConsumer.handler",
            code=_lambda.Code.from_asset("lambda_functions/extract"),
            reserved_concurrent_executions=self.lambda_throttle_size,
            environment={
                "CLUSTER_NAME": self.ecs_cluster.cluster_name,
                "TASK_DEFINITION": self.task_definition.task_definition_arn,
                "SUBNETS": json.dumps(self.subnet_ids),
                "CONTAINER_NAME": self.extraction_task.container_name
            }
        )
        extractor.add_event_source(
            lambda_event_sources.SqsEventSource(queue=self.upload_queue)
        )

        for policy in (
            self.create_iam_policy(
                resources=[self.task_definition.task_definition_arn],
                actions=['ecs:RunTask']
            ),
            self.create_iam_policy(
                resources=[
                    self.task_definition.obtain_execution_role().role_arn,
                    self.task_definition.task_role.role_arn
                ],
                actions=['iam:PassRole']
            )
        ):
            extractor.add_to_role_policy(policy)



        ####
        # Transform
        # defines a lambda to transform the data that was extracted from s3
        ####

        # transformer = _lambda.Function(
        #     self, "TransformLambdaHandler",
        #     runtime=_lambda.Runtime.NODEJS_12_X,
        #     handler="transform.handler",
        #     code=_lambda.Code.from_asset("lambda_functions/transform"),
        #     reserved_concurrent_executions=self.lambda_throttle_size,
        #     timeout=cdk.Duration.seconds(3)
        # )

        transformer = self.create_lambda_function()(
            logical_name="TransformLambdaHandler",
            function="transform",
        )



        self.create_event_bridge_rule(
            name='transform',
            description='Data extracted from S3, Needs transformation',
            detail_type='s3RecordExtraction',
            status="extracted",
            lambda_function=transformer,
        )

        ####
        # Load
        # load the transformed data in dynamodb
        ####
        loader = self.create_lambda_function(
            logical_name="LoadLambdaHandler",
            function_name="load",
            environment_variables={
                "TABLE_NAME": self.transformed_data.table_name
            }
        )


        self.create_event_bridge_rule(
            name='load',
            description='Load Transformed Data to DynamoDB',
            detail_type='transform',
            status="transformed",
            lambda_function=loader,
        )

        self.add_policies_to_lambda_functions(
            extractor, transformer, loader,
            policy=self.event_bridge_put_policy
        )

        self.upload_queue.grant_consume_messages(extractor)
        self.transformed_data.grant_read_write_data(loader)
        ####
        # Observe
        # Watch for all cdkpatterns.the-eventbridge-etl events and log them centrally
        ####
        observer = self.create_lambda_function(
            logical_name="ObserveLam bdaHandler",
            function_name="observe",
        )

        self.create_event_bridge_rule(
            name='observe',
            description='all events are caught here and logged centrally',
            lambda_function=observer,
        )

    def create_lambda_function(self, logical_name=None, function_name=None, concurrent_executions=2, timeout=3, environment_variables=None):
        return _lambda.Function(
            self, logical_name,
            runtime=_lambda.Runtime.NODEJS_12_X,
            handler=f'{function_name}.handler',
            code=_lambda.Code.from_asset(f'lambda_functions/{function_name}'),
            reserved_concurrent_executions=concurrent_executions,
            timeout=cdk.Duration.seconds(timeout),
            environment=environment_variables,
        )

    def create_dynamodb_table(self):
        return dynamodb_table.DynamoDBTableConstruct(
            self, 'TransformedData',
            partition_key=dynamo_db.Attribute(
                name="id",
                type=dynamo_db.AttributeType.STRING
            )
        ).dynamodb_table

    def create_sqs_queue(self):
        return sqs.Queue(
            self, 'newObjectInLandingBucketEventQueue',
            visibility_timeout=cdk.Duration.seconds(300)
        )

    @staticmethod
    def create_s3_sqs_notification(bucket=None, sqs_queue=None):
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.SqsDestination(sqs_queue)
        )

    @staticmethod
    def create_iam_policy(resources=None, actions=None):
        return iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=resources if resources else ["*"],
            actions=actions
        )

    def create_event_bridge_iam_policy(self):
        return self.create_iam_policy(actions=['events:PutEvents'])

    def create_event_bridge_rule(
        self, name=None, description=None, detail_type=None, status=None,
        lambda_function=None
    ):
        rule = events.Rule(
            self, f'{name}Rule',
            description=description,
            event_pattern=events.EventPattern(
                source=['cdkpatterns.the-eventbridge-etl'],
                detail_type=[detail_type] if detail_type else None,
                detail={"status": [status]} if status else None
            )
        )
        rule.add_target(
            event_bridge_targets.LambdaFunction(handler=lambda_function)
        )
        return rule

    def add_policies_to_lambda_functions(self, *lambda_functions, policy=None):
        for lambda_function in lambda_functions:
            lambda_function.add_to_role_policy(policy)