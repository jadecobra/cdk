import json
import aws_cdk
import constructs
import well_architected
import well_architected_constructs.dynamodb_table
import well_architected_constructs.lambda_function


# s3_sqs_lambda_ecs_eventbridge_lambda_dynamodb
class EventbridgeEtl(well_architected.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.s3_bucket = self.create_s3_bucket()
        self.dynamodb_table = self.create_dynamodb_table(self.error_topic)
        self.sqs_queue = self.create_sqs_queue()
        self.add_sqs_event_notification_to_bucket(
            bucket=self.s3_bucket,
            sqs_queue=self.sqs_queue,
        )

        ####
        # Fargate ECS Task Creation to pull data from S3
        ####
        self.vpc = self.create_vpc()
        self.ecs_cluster = self.create_ecs_cluster(self.vpc)
        self.ecs_task_definition = self.create_ecs_task_definition()
        self.ecs_task_definition.add_to_task_role_policy(self.event_bridge_iam_policy())
        self.s3_bucket.grant_read(self.ecs_task_definition.task_role)

        self.extractor = self.create_lambda_function(
            function_name='extractor',
            error_topic=self.error_topic,
            environment_variables={
                "CLUSTER_NAME": self.ecs_cluster.cluster_name,
                "TASK_DEFINITION": self.ecs_task_definition.task_definition_arn,
                "SUBNETS": self.get_subnet_ids(self.vpc),
                "CONTAINER_NAME": self.ecs_task_definition.add_container(
                    'AppContainer',
                    image=aws_cdk.aws_ecs.ContainerImage.from_asset('containers/s3DataExtractionTask'),
                    logging=self.get_logging_configuration(),
                    environment={
                        'S3_BUCKET_NAME': self.s3_bucket.bucket_name,
                        'S3_OBJECT_KEY': ''
                    }
                ).container_name
            }
        )

        self.transformer = self.create_lambda_function(
            function_name='transformer',
            error_topic=self.error_topic,
            event_bridge_rule_description='Data extracted from S3, Needs transformation',
            event_bridge_detail_type='s3RecordExtraction',
            event_bridge_detail_status="extracted",
        )

        self.loader = self.create_lambda_function(
            function_name="loader",
            error_topic=self.error_topic,
            environment_variables={
                "TABLE_NAME": self.dynamodb_table.table_name
            },
            event_bridge_rule_description='Load Transformed Data to DynamoDB',
            event_bridge_detail_type='transform',
            event_bridge_detail_status="transformed",
        )

        self.create_lambda_function(
            function_name="observer",
            error_topic=self.error_topic,
            event_bridge_rule_description='observe and log all events'
        )

        # IAM
        self.grant_ecs_task_permissions(
            ecs_task_definition=self.ecs_task_definition,
            lambda_function=self.extractor
        )
        self.add_policies_to_lambda_functions(
            self.extractor,
            self.transformer,
            self.loader,
            policy=self.event_bridge_iam_policy()
        )

        self.extractor.add_event_source(
            aws_cdk.aws_lambda_event_sources.SqsEventSource(queue=self.sqs_queue)
        )
        self.sqs_queue.grant_consume_messages(self.extractor)
        self.dynamodb_table.grant_read_write_data(self.loader)

    def create_s3_bucket(self):
        return aws_cdk.aws_s3.Bucket(self, "LandingBucket")

    def create_vpc(self):
        return aws_cdk.aws_ec2.Vpc(self, "Vpc", max_azs=2)

    def create_ecs_cluster(self, vpc):
        return aws_cdk.aws_ecs.Cluster(self, 'EcsCluster', vpc=vpc)

    def create_ecs_task_definition(self):
        return aws_cdk.aws_ecs.TaskDefinition(
            self, 'FargateTaskDefinition',
            memory_mib="512",
            cpu="256",
            compatibility=aws_cdk.aws_ecs.Compatibility.FARGATE
        )

    def create_event_bridge_rule(
        self, name=None, description=None, detail_type=None, status=None,
    ):
        return aws_cdk.aws_events.Rule(
            self, f'{name}Rule',
            description=description,
            event_pattern=aws_cdk.aws_events.EventPattern(
                source=['cdkpatterns.the-eventbridge-etl'],
                detail_type=[detail_type] if detail_type else None,
                detail={"status": [status]} if status else None
            )
        )

    def create_lambda_function(
        self,
        function_name=None,
        error_topic=None,
        concurrent_executions=2,
        duration=3,
        environment_variables=None,
        event_bridge_rule_description=None,
        event_bridge_detail_type=None,
        event_bridge_detail_status=None
    ):
        return well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, function_name,
            function_name=function_name,
            error_topic=error_topic,
            concurrent_executions=concurrent_executions,
            duration=duration,
            environment_variables=environment_variables,
            event_bridge_rule=self.create_event_bridge_rule(
                name=function_name,
                description=event_bridge_rule_description,
                detail_type=event_bridge_detail_type,
                status=event_bridge_detail_status,
            )
        ).lambda_function

    def create_dynamodb_table(self, error_topic):
        return well_architected_constructs.dynamodb_table.DynamoDBTableConstruct(
            self, 'TransformedData',
            error_topic=error_topic,
            partition_key="id",
        ).dynamodb_table

    def create_sqs_queue(self):
        return aws_cdk.aws_sqs.Queue(
            self,
            'newObjectInLandingBucketEventQueue',
            visibility_timeout=aws_cdk.Duration.seconds(300)
        )

    @staticmethod
    def add_sqs_event_notification_to_bucket(
        bucket=None, sqs_queue=None
    ):
        bucket.add_event_notification(
            aws_cdk.aws_s3.EventType.OBJECT_CREATED,
            aws_cdk.aws_s3_notifications.SqsDestination(sqs_queue)
        )

    @staticmethod
    def create_iam_policy(resources=None, actions=None):
        return aws_cdk.aws_iam.PolicyStatement(
            effect=aws_cdk.aws_iam.Effect.ALLOW,
            resources=resources if resources else ["*"],
            actions=actions
        )

    def event_bridge_iam_policy(self):
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
    def get_logging_configuration():
        return aws_cdk.aws_ecs.AwsLogDriver(
            stream_prefix='TheEventBridgeETL',
            log_retention=aws_cdk.aws_logs.RetentionDays.ONE_WEEK
        )