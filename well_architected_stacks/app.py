import aws_cdk
import src.well_architected_stacks as well_architected_stacks
import src.well_architected_stacks.lambda_trilogy as lambda_trilogy
import src.well_architected_stacks.simple_graphql_service.simple_graphql_service as simple_graphql_service
# import src.regular_stacks.ecs

import os

class WellArchitected(aws_cdk.App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lambda_directory = '../lambda_functions'
        self.create_well_architected_stacks()
        self.lambda_trilogy()
        self.xray_tracer()
        # self.ecs()
        # self.in_progress()

    def api_lambda_dynamodb(self):
        well_architected_stacks.api_lambda_dynamodb.ApiLambdaDynamodbStack(
            self, 'HttpApiLambdaDynamodb',
            function_name='hit_counter',
            partition_key='path',
            lambda_directory=self.lambda_directory,
            create_http_api=True,
        )
        well_architected_stacks.api_lambda_dynamodb.ApiLambdaDynamodbStack(
            self, 'RestApiLambdaDynamodb',
            function_name='hit_counter',
            partition_key='path',
            lambda_directory=self.lambda_directory,
            create_rest_api=True,
        )

    def api_lambda_dynamodb_eventbridge(self):
        well_architected_stacks.api_lambda_dynamodb_eventbridge_lambda.ApiLambdaDynamodbEventBridgeLambda(
            self, 'HttpApiLambdaDynamodbEventBridgeLambda',
            lambda_directory=self.lambda_directory,
            create_http_api=True
        )

        well_architected_stacks.api_lambda_dynamodb_eventbridge_lambda.ApiLambdaDynamodbEventBridgeLambda(
            self, 'RestApiLambdaDynamodbEventBridgeLambda',
            lambda_directory=self.lambda_directory,
            create_rest_api=True,
        )

    def api_lambda_eventbridge_lambda(self):
        well_architected_stacks.api_lambda_eventbridge_lambda.ApiLambdaEventBridgeLambda(
            self, 'HttpApiLambdaEventBridgeLambda',
            lambda_directory=self.lambda_directory,
            create_http_api=True,
        )
        well_architected_stacks.api_lambda_eventbridge_lambda.ApiLambdaEventBridgeLambda(
            self, 'RestApiLambdaEventBridgeLambda',
            lambda_directory=self.lambda_directory,
            create_rest_api=True,
        )

    def api_lambda_rds(self):
        well_architected_stacks.api_lambda_rds.ApiLambdaRds(
            self, 'HttpApiLambdaRds',
            lambda_directory=self.lambda_directory,
            create_http_api=True,
        )
        well_architected_stacks.api_lambda_rds.ApiLambdaRds(
            self, 'RestApiLambdaRds',
            lambda_directory=self.lambda_directory,
            create_rest_api=True,
        )

    def api_lambda_sqs_lambda_dynamodb(self):
        well_architected_stacks.api_lambda_sqs_lambda_dynamodb.ApiLambdaSqsLambdaDynamodb(
            self, 'HttpApiLambdaSqsLambdaDynamodb',
            lambda_directory=self.lambda_directory,
            create_http_api=True,
        )
        well_architected_stacks.api_lambda_sqs_lambda_dynamodb.ApiLambdaSqsLambdaDynamodb(
            self, 'RestApiLambdaSqsLambdaDynamodb',
            lambda_directory=self.lambda_directory,
            create_rest_api=True,
        )

    def api_step_functions(self):
        well_architected_stacks.api_step_functions.ApiStepFunctionsStack(
            self, 'HttpApiStepFunctions',
            lambda_directory=self.lambda_directory,
            create_http_api=True,
        )
        well_architected_stacks.api_step_functions.ApiStepFunctionsStack(
            self, 'RestApiStepFunctions',
            lambda_directory=self.lambda_directory,
            create_rest_api=True,
        )

    def api_saga_step_functions(self):
        well_architected_stacks.saga_step_function.SagaStepFunction(
            self, 'HttpApiSagaStepFunction',
            lambda_directory=self.lambda_directory,
            create_http_api=True,
        )
        well_architected_stacks.saga_step_function.SagaStepFunction(
            self, 'RestApiSagaStepFunction',
            lambda_directory=self.lambda_directory,
            create_rest_api=True,
        )

    def lambda_power_tuner(self):
        well_architected_stacks.lambda_power_tuner.LambdaPowerTuner(
            self, 'LambdaPowerTuner',
            lambda_directory=self.lambda_directory,
        )


    def rest_api_stacks(self):
        well_architected_stacks.rest_api_dynamodb.RestApiDynamodb(
            self, 'RestApiDynamodb',
            partition_key='message',
            lambda_directory=self.lambda_directory,
        )
        well_architected_stacks.rest_api_sns_lambda_eventbridge_lambda.RestApiSnsLambdaEventBridgeLambda(
            self, 'RestApiSnsLambdaEventBridgeLambda',
            lambda_directory=self.lambda_directory,
        )
        well_architected_stacks.rest_api_sns_sqs_lambda.RestApiSnsSqsLambda(
            self, 'RestApiSnsSqsLambda',
            lambda_directory=self.lambda_directory,
        )

    def misc(self):
        well_architected_stacks.s3_sqs_lambda_ecs_eventbridge_lambda_dynamodb.S3SqsLambdaEcsEventBridgeLambdaDynamodb(
            self, 'S3SqsLambdaEcsEventBridgeLambdaDynamodb',
            lambda_directory=self.lambda_directory,
            containers_directory='../containers',
        )

        simple_graphql_service.SimpleGraphQlService(
            self, 'SimpleGraphqlService',
            lambda_directory=self.lambda_directory,
        )
        well_architected_stacks.waf_rest_api_lambda_dynamodb.WafApiLambdaDynamodb(
            self, 'WafRestApiLambdaDynamodb',
            lambda_directory=self.lambda_directory,
            function_name='hit_counter',
            partition_key='path',
            create_rest_api=True,
        )

    def create_well_architected_stacks(self):
        self.api_lambda_dynamodb()
        self.api_lambda_dynamodb_eventbridge()
        self.api_lambda_eventbridge_lambda()
        self.api_lambda_rds()
        self.api_lambda_sqs_lambda_dynamodb()
        self.api_step_functions()
        self.lambda_power_tuner()
        self.rest_api_stacks()
        self.misc()
        # self.api_saga_step_functions() # Fix this. Do StepFunctions examples
        return

    def lambda_trilogy(self):
        well_architected_stacks.lambda_trilogy.lambda_lith.LambdaLith(
            self, "HttpApiLambdaLith",
            function_name='lambda_lith',
            lambda_directory=self.lambda_directory,
            create_http_api=True,
        )
        well_architected_stacks.lambda_trilogy.lambda_lith.LambdaLith(
            self, "RestApiLambdaLith",
            function_name='lambda_lith',
            lambda_directory=self.lambda_directory,
            create_rest_api=True,
        )
        well_architected_stacks.lambda_trilogy.lambda_trilogy.LambdaTrilogy(
            self, 'HttpApiLambdaFat',
            function_name='lambda_fat',
            lambda_directory=self.lambda_directory,
            create_http_api=True,
        )
        well_architected_stacks.lambda_trilogy.lambda_trilogy.LambdaTrilogy(
            self, 'RestApiLambdaFat',
            function_name='lambda_fat',
            lambda_directory=self.lambda_directory,
            create_rest_api=True,
        )
        well_architected_stacks.lambda_trilogy.lambda_trilogy.LambdaTrilogy(
            self, 'HttpApiLambdaSinglePurpose',
            function_name='lambda_single_purpose',
            lambda_directory=self.lambda_directory,
            create_http_api=True,
        )
        well_architected_stacks.lambda_trilogy.lambda_trilogy.LambdaTrilogy(
            self, 'RestApiLambdaSinglePurpose',
            function_name='lambda_single_purpose',
            lambda_directory=self.lambda_directory,
            create_rest_api=True,
        )

    def xray_tracer(self):
        xray_tracer_sns_topic = well_architected_stacks.sns_topic.SnsTopic(
            self, 'XRayTracerSnsTopic', display_name='XRayTracerSnsTopic',
        )
        xray_tracer_error_topic = well_architected_stacks.sns_topic.SnsTopic(
            self, 'XRayTracerErrorTopic', display_name='XRayTracerErrorTopic',
        )
        well_architected_stacks.rest_api_sns.RestApiSnsStack(
            self, 'RestApiSns',
            sns_topic_arn=xray_tracer_sns_topic.sns_topic.topic_arn,
            error_topic=xray_tracer_error_topic.sns_topic,
            lambda_directory=self.lambda_directory,
        )
        well_architected_stacks.sns_lambda_sns.SnsLambdaSns(
            self, 'SnsLambdaSns',
            sns_publisher_trigger=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_error_topic.sns_topic,
            lambda_directory=self.lambda_directory,
            publisher_lambda_name='sns_publisher',
            subscriber_lambda_name='sns_subscriber',
        )
        well_architected_stacks.sqs_lambda_sqs.SqsLambdaSqs(
            self, 'SqsLambdaSqs',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_error_topic.sns_topic,
            lambda_directory=self.lambda_directory,
        )
        # well_architected_stacks.sns_lambda.SnsLambda(
        #     self, 'SnsLambda',
        #     sns_topic_arn=xray_tracer_sns_topic.sns_topic.topic_arn,
        #     error_topic=xray_tracer_error_topic.sns_topic,
        #     lambda_directory=self.lambda_directory,
        #     lambda_function_name="sns_lambda",
        # )
        # well_architected_stacks.sns_lambda_dynamodb.SnsLambdaDynamodb(
        #     self, 'SnsLambdaDynamodb',
        #     partition_key="path",
        #     lambda_function_name="hit_counter",
        #     sns_topic_arn=xray_tracer_sns_topic.sns_topic.topic_arn,
        #     error_topic=xray_tracer_error_topic.sns_topic,
        #     lambda_directory=self.lambda_directory,
        # )

    def ecs(self):
        return
        def container_image():
            return "amazon/amazon-ecs-sample"

        stacks.ecs.autoscaling_ecs_cluster.AutoscalingEcsCluster(
            self, 'AutoscalingEcsCluster',
        )
        stacks.ecs.autoscaling_ecs_service.AutoscalingEcsService(
            self, 'AutoscalingEcsService',
            container_image='nginx:latest',
        )
        stacks.ecs.autoscaling_ecs_service_with_placement.AutoscalingEcsServiceWithPlacement(
            self, 'AutoscalingEcsServiceWithPlacement',
            container_image='nginx:latest',
        )
        stacks.ecs.alb_autoscaling_ecs_service.AlbAutoscalingEcsService(
            self, 'AlbAutoscalingEcsService',
            container_image=container_image(),
        )
        stacks.ecs.nlb_autoscaling_ecs_service.NlbAutoscalingEcsService(
            self, 'NlbAutoscalingEcsService',
            container_image=container_image(),
        )
        stacks.ecs.nlb_fargate_service.NlbFargateService(
            self, 'NlbFargateService',
            container_image=container_image(),
        )
        stacks.ecs.nlb_autoscaling_fargate_service.NlbAutoscalingFargateService(
            self, 'NlbAutoscalingFargateService',
            container_image=container_image()
        )

WellArchitected().synth()

# TODO
# Add Metrics/Alarms for
# - RDS
# - StateMachine
# - WAF
# ApiSagaStepFunctions
# Error Rate over time - Total Errors / Total Invocations
# StateMachine examples - https://docs.aws.amazon.com/step-functions/latest/dg/create-sample-projects.html
# Add Lambda Powertools layer