import json
import aws_cdk
import constructs
import dynamodb_table

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
)


class EventbridgeEtl(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
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
        ####
        self.vpc = ec2.Vpc(self, "Vpc", max_azs=2)
        self.ecs_cluster = ecs.Cluster(self, 'Ec2Cluster', vpc=self.vpc)
        self.ecs_task_definition = ecs.TaskDefinition(
            self, 'FargateTaskDefinition',
            memory_mib="512",
            cpu="256",
            compatibility=ecs.Compatibility.FARGATE
        )
        self.ecs_task_definition.add_to_task_role_policy(self.event_bridge_put_policy)
        self.upload_bucket.grant_read(self.ecs_task_definition.task_role)

        self.extraction_task = self.ecs_task_definition.add_container(
            'AppContainer',
            image=ecs.ContainerImage.from_asset('containers/s3DataExtractionTask'),
            logging=self.logging(),
            environment={
                'S3_BUCKET_NAME': self.upload_bucket.bucket_name,
                'S3_OBJECT_KEY': ''
            }
        )

        self.extractor = self.create_lambda_function(
            function_name='extractor',
            environment_variables={
                "CLUSTER_NAME": self.ecs_cluster.cluster_name,
                "TASK_DEFINITION": self.ecs_task_definition.task_definition_arn,
                "SUBNETS": self.get_subnet_ids(self.vpc),
                "CONTAINER_NAME": self.extraction_task.container_name
            }
        )

        self.transformer = self.create_lambda_function(
            function_name='transformer',
            event_bridge_rule_description='Data extracted from S3, Needs transformation',
            event_bridge_detail_type='s3RecordExtraction',
            event_bridge_detail_status="extracted",
        )

        self.loader = self.create_lambda_function(
            function_name="loader",
            environment_variables={
                "TABLE_NAME": self.transformed_data.table_name
            },
            event_bridge_rule_description='Load Transformed Data to DynamoDB',
            event_bridge_detail_type='transform',
            event_bridge_detail_status="transformed",
        )

        self.create_lambda_function(
            function_name="observer",
            event_bridge_rule_description='observe and log all events'
        )

        # IAM
        self.grant_ecs_task_permissions(
            ecs_task_definition=self.ecs_task_definition,
            lambda_function=self.extractor
        )
        self.add_policies_to_lambda_functions(
            self.extractor, self.transformer, self.loader,
            policy=self.event_bridge_put_policy
        )

        self.extractor.add_event_source(
            lambda_event_sources.SqsEventSource(queue=self.upload_queue)
        )
        self.upload_queue.grant_consume_messages(self.extractor)
        self.transformed_data.grant_read_write_data(self.loader)

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

    def create_lambda_function(
        self, function_name=None,
        concurrent_executions=2, timeout=3, environment_variables=None,
        event_bridge_rule_description=None,
        event_bridge_detail_type=None,
        event_bridge_detail_status=None
    ):
        lambda_function = _lambda.Function(
            self, function_name,
            runtime=_lambda.Runtime.NODEJS_12_X,
            handler=f'{function_name}.handler',
            code=_lambda.Code.from_asset(f'lambda_functions/{function_name}'),
            reserved_concurrent_executions=concurrent_executions,
            timeout=aws_cdk.Duration.seconds(timeout),
            environment=environment_variables,
        )
        if event_bridge_rule_description:
            self.create_event_bridge_rule(
                name=function_name,
                description=event_bridge_rule_description,
                detail_type=event_bridge_detail_type,
                status=event_bridge_detail_status,
                lambda_function=lambda_function,
            )
        return lambda_function

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
            visibility_timeout=aws_cdk.Duration.seconds(300)
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

    def add_policies_to_lambda_functions(self, *lambda_functions, policy=None):
        for lambda_function in lambda_functions:
            lambda_function.add_to_role_policy(policy)

    def grant_ecs_task_permissions(self, ecs_task_definition=None, lambda_function=None):
        for policy in (
            self.create_iam_policy(
                resources=[ecs_task_definition.task_definition_arn],
                actions=['ecs:RunTask']
            ),
            self.create_iam_policy(
                resources=[
                    ecs_task_definition.obtain_execution_role().role_arn,
                    ecs_task_definition.task_role.role_arn
                ],
                actions=['iam:PassRole']
            )
        ):
            self.add_policies_to_lambda_functions(lambda_function, policy=policy)

    @staticmethod
    def get_subnet_ids(vpc):
        return json.dumps([subnet.subnet_id for subnet in vpc.private_subnets])

    @staticmethod
    def logging():
        return ecs.AwsLogDriver(
            stream_prefix='TheEventBridgeETL',
            log_retention=logs.RetentionDays.ONE_WEEK
        )