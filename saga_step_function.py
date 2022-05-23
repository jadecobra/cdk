import aws_cdk
import constructs
import well_architected
import well_architected_constructs.lambda_function
import well_architected_constructs.dynamodb_table

from aws_cdk import (
    aws_lambda,
    aws_apigateway,
    aws_dynamodb as dynamo_db,
    aws_stepfunctions,
    aws_stepfunctions_tasks,
)


class SagaStepFunction(well_architected.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bookings = well_architected_constructs.dynamodb_table.DynamoDBTableConstruct(
            self, 'DynamodbTable',
            partition_key='booking_id',
            sort_key='booking_type',
            error_topic=self.error_topic,
        ).dynamodb_table

        flight_reservation_function = self.create_lambda_function(
            self,
            function_name='flights/reserve_flight',
            table=bookings,
            error_topic=self.error_topic,
        )
        flight_confirmation_function = self.create_lambda_function(
            self,
            function_name='flights/confirm_flight',
            table=bookings,
            error_topic=self.error_topic,
        )
        flight_cancellation_function = self.create_lambda_function(
            self,
            function_name='flights/cancel_flight',
            table=bookings,
            error_topic=self.error_topic,
        )

        hotel_reservation_function = self.create_lambda_function(
            self,
            function_name="hotels/reserve_hotel",
            table=bookings,
            error_topic=self.error_topic,
        )

        hotel_confirmation_function = self.create_lambda_function(
            self,
            function_name='hotels/confirm_hotel',
            table=bookings,
            error_topic=self.error_topic,
        )

        hotel_cancellation_function = self.create_lambda_function(
            self,
            function_name="hotels/cancel_hotel",
            table=bookings,
            error_topic=self.error_topic,
        )

        payment_processing_function = self.create_lambda_function(
            self,
            function_name="payments/process_payment",
            table=bookings,
            error_topic=self.error_topic,
        )

        payment_refund_function = self.create_lambda_function(
            self,
            function_name="payments/refund_payment",
            table=bookings,
            error_topic=self.error_topic,
        )

        ###
        # Saga Pattern Step Function
        ###
        # Follows a strict order:
        # 1) Reserve Flights and Hotel
        # 2) Take Payment
        # 3) Confirm Flight and Hotel booking

        # 1) Reserve Flights and Hotel
        cancel_hotel_reservation = self.create_cancellation_task(
            task_name='CancelHotelReservation',
            lambda_function=hotel_cancellation_function,
            next_step=aws_stepfunctions.Fail(
                self, "Sorry, We Couldn't make the booking"
            )
        )

        cancel_flight_reservation = self.create_cancellation_task(
            task_name='CancelFlightReservation',
            lambda_function=flight_cancellation_function,
            next_step=cancel_hotel_reservation,
        )

        refund_payment = self.create_cancellation_task(
            task_name='RefundPayment',
            lambda_function=payment_refund_function,
            next_step=cancel_flight_reservation
        )

        saga_state_machine = aws_stepfunctions.StateMachine(
            self, 'StateMachine',
            definition=(
                aws_stepfunctions
                    .Chain
                    .start(
                        self.create_step_function_task_with_error_handler(
                            task_name='ReserveHotel',
                            lambda_function=hotel_reservation_function,
                            error_handler=cancel_hotel_reservation,
                        )
                    )
                    .next(
                        self.create_step_function_task_with_error_handler(
                            task_name='ReserveFlight',
                            lambda_function=flight_reservation_function,
                            error_handler=cancel_flight_reservation,
                        )
                    )
                    .next(
                        self.create_step_function_task_with_error_handler(
                            task_name='TakePayment',
                            lambda_function=payment_processing_function,
                            error_handler=refund_payment,
                        )
                    )
                    .next(
                        self.create_step_function_task_with_error_handler(
                            task_name='ConfirmHotelBooking',
                            lambda_function=hotel_confirmation_function,
                            error_handler=refund_payment,
                        )
                    )
                    .next(
                        self.create_step_function_task_with_error_handler(
                            task_name='ConfirmFlight',
                            lambda_function=flight_confirmation_function,
                            error_handler=refund_payment,
                        )
                    )
                    .next(
                        aws_stepfunctions.Succeed(self, 'We have made your booking!')
                    )
            ),
            timeout=aws_cdk.Duration.minutes(5)
        )

        saga_lambda = well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, 'SagaLambdaFUnction',
            error_topic=self.error_topic,
            function_name='saga_lambda',
            environment_variables={
                'statemachine_arn': saga_state_machine.state_machine_arn
            },
        ).lambda_function

        saga_state_machine.grant_start_execution(saga_lambda)

        aws_apigateway.LambdaRestApi(
            self, 'SagaLambdaFunctionRestApi',
            handler=saga_lambda
        )

    def create_cancellation_task(self, task_name=None, lambda_function=None, next_step=None):
        return aws_stepfunctions_tasks.LambdaInvoke(
            self, task_name,
            lambda_function=lambda_function,
            result_path=f'$.{task_name}Result'
        ).add_retry(
            max_attempts=3
        ).next(
            next_step
        )

    def create_step_function_task_with_error_handler(self, task_name=None, lambda_function=None, error_handler=None):
        return aws_stepfunctions_tasks.LambdaInvoke(
            self, task_name,
            lambda_function=lambda_function,
            result_path=f'$.{task_name}Result'
        ).add_catch(
            error_handler,
            result_path=f"$.{task_name}Error"
        )

    def create_lambda_function(self, scope: aws_cdk.Stack, table: dynamo_db.Table=None, function_name=None, error_topic=None):
        function = well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, function_name,
            function_name=function_name,
            error_topic=error_topic,
            environment_variables={
                'TABLE_NAME': table.table_name
            }
        ).lambda_function
        table.grant_read_write_data(function)
        return function