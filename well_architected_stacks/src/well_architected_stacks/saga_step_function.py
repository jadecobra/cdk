import aws_cdk
import constructs
import well_architected_constructs

from . import well_architected_stack


class SagaStepFunction(well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        self.dynamodb_construct = well_architected_constructs.dynamodb_table.DynamodbTable(
            self, 'DynamodbTable',
            partition_key='booking_id',
            sort_key='booking_type',
            error_topic=self.error_topic,
        )
        bookings_record = self.dynamodb_construct.dynamodb_table

        flight_reservation_function = self.create_bookings_lambda_function(
            function_name='flights/reserve_flight',
            table=bookings_record,
        )
        flight_confirmation_function = self.create_bookings_lambda_function(
            function_name='flights/confirm_flight',
            table=bookings_record,
        )
        flight_cancellation_function = self.create_bookings_lambda_function(
            function_name='flights/cancel_flight',
            table=bookings_record,
        )

        hotel_reservation_function = self.create_bookings_lambda_function(
            function_name="hotels/reserve_hotel",
            table=bookings_record,
        )

        hotel_confirmation_function = self.create_bookings_lambda_function(
            function_name='hotels/confirm_hotel',
            table=bookings_record,
        )

        hotel_cancellation_function = self.create_bookings_lambda_function(
            function_name="hotels/cancel_hotel",
            table=bookings_record,
        )

        payment_processing_function = self.create_bookings_lambda_function(
            function_name="payments/process_payment",
            table=bookings_record,
        )

        payment_refund_function = self.create_bookings_lambda_function(
            function_name="payments/refund_payment",
            table=bookings_record,
        )

        '''
        Saga Step Function Follows a strict order:
        1) Reserve Flights and Hotel
        2) Take Payment
        3) Confirm Flight and Hotel booking
        '''

        # 1) Reserve Flights and Hotel
        cancel_hotel_reservation = self.create_cancellation_task(
            task_name='CancelHotelReservation',
            lambda_function=hotel_cancellation_function,
            next_step=aws_cdk.aws_stepfunctions.Fail(
                self, "Sorry, We Couldn't make the booking"
            )
        )

        cancel_flight_reservation = self.create_cancellation_task(
            task_name='CancelFlightReservation',
            lambda_function=flight_cancellation_function.lambda_function,
            next_step=cancel_hotel_reservation,
        )

        refund_payment = self.create_cancellation_task(
            task_name='RefundPayment',
            lambda_function=payment_refund_function.lambda_function,
            next_step=cancel_flight_reservation
        )


        # self.state_machine = aws_cdk.aws_stepfunctions.StateMachine(
        #     self, 'StateMachine',
        #     definition=(
        #         aws_cdk.aws_stepfunctions.Chain
        #             .start(
        #                 self.create_step_function_task_with_error_handler(
        #                     task_name='ReserveHotel',
        #                     lambda_function=hotel_reservation_function.lambda_function,
        #                     error_handler=cancel_hotel_reservation,
        #                 )
        #             )
        #             .next(
        #                 self.create_step_function_task_with_error_handler(
        #                     task_name='ReserveFlight',
        #                     lambda_function=flight_reservation_function.lambda_function,
        #                     error_handler=cancel_flight_reservation,
        #                 )
        #             )
        #             .next(
        #                 self.create_step_function_task_with_error_handler(
        #                     task_name='TakePayment',
        #                     lambda_function=payment_processing_function.lambda_function,
        #                     error_handler=refund_payment,
        #                 )
        #             )
        #             .next(
        #                 self.create_step_function_task_with_error_handler(
        #                     task_name='ConfirmHotelBooking',
        #                     lambda_function=hotel_confirmation_function.lambda_function,
        #                     error_handler=refund_payment,
        #                 )
        #             )
        #             .next(
        #                 self.create_step_function_task_with_error_handler(
        #                     task_name='ConfirmFlight',
        #                     lambda_function=flight_confirmation_function.lambda_function,
        #                     error_handler=refund_payment,
        #                 )
        #             )
        #             .next(
        #                 aws_cdk.aws_stepfunctions.Succeed(
        #                     self, 'We have made your booking!'
        #                 )
        #             )
        #     ),
        #     timeout=aws_cdk.Duration.minutes(5),
        #     tracing_enabled=True,
        #     state_machine_type=aws_cdk.aws_stepfunctions.StateMachineType.EXPRESS,
        # )

        self.step_api_function = well_architected_constructs.api_step_functions.ApiStepFunctions(
            self, 'ApiStepFunctions',
            error_topic=self.error_topic,
            create_http_api=self.create_http_api,
            create_rest_api=self.create_rest_api,
            state_machine_definition=(
                aws_cdk.aws_stepfunctions.Chain
                    .start(
                        self.create_step_function_task_with_error_handler(
                            task_name='ReserveHotel',
                            lambda_function=hotel_reservation_function.lambda_function,
                            error_handler=cancel_hotel_reservation,
                        )
                    )
                    .next(
                        self.create_step_function_task_with_error_handler(
                            task_name='ReserveFlight',
                            lambda_function=flight_reservation_function.lambda_function,
                            error_handler=cancel_flight_reservation,
                        )
                    )
                    .next(
                        self.create_step_function_task_with_error_handler(
                            task_name='TakePayment',
                            lambda_function=payment_processing_function.lambda_function,
                            error_handler=refund_payment,
                        )
                    )
                    .next(
                        self.create_step_function_task_with_error_handler(
                            task_name='ConfirmHotelBooking',
                            lambda_function=hotel_confirmation_function.lambda_function,
                            error_handler=refund_payment,
                        )
                    )
                    .next(
                        self.create_step_function_task_with_error_handler(
                            task_name='ConfirmFlight',
                            lambda_function=flight_confirmation_function.lambda_function,
                            error_handler=refund_payment,
                        )
                    )
                    .next(
                        aws_cdk.aws_stepfunctions.Succeed(
                            self, 'We have made your booking!'
                        )
                    )
            )
        )


        self.state_machine = self.step_api_function.state_machine
        self.saga_lambda = self.create_lambda_construct(
            function_name='saga_lambda',
            environment_variables={
                'statemachine_arn': self.state_machine.state_machine_arn
            },
        )

        self.state_machine.grant_start_execution(self.saga_lambda.lambda_function)
        flight_reservation_function.lambda_function.grant_invoke(self.state_machine.role)
        self.create_cloudwatch_dashboard(
            *self.dynamodb_construct.create_cloudwatch_widgets(),
            *self.saga_lambda.create_cloudwatch_widgets(),
            *self.step_api_function.api_construct.create_cloudwatch_widgets(),
            *flight_reservation_function.create_cloudwatch_widgets(),
            *flight_confirmation_function.create_cloudwatch_widgets(),
            *flight_cancellation_function.create_cloudwatch_widgets(),
            *hotel_reservation_function.create_cloudwatch_widgets(),
            *hotel_confirmation_function.create_cloudwatch_widgets(),
            *hotel_cancellation_function.create_cloudwatch_widgets(),
            *payment_processing_function.create_cloudwatch_widgets(),
            *payment_refund_function.create_cloudwatch_widgets(),
        )

    def create_stepfunctions_task(
        self, task_name=None, lambda_function=None
    ):
        return aws_cdk.aws_stepfunctions_tasks.LambdaInvoke(
            self, task_name,
            lambda_function=lambda_function,
            result_path=f'$.{task_name}Result'
        )

    def create_cancellation_task(
        self, task_name=None, lambda_function=None, next_step=None
    ):
        return self.create_stepfunctions_task(
            task_name=task_name,
            lambda_function=lambda_function,
        ).add_retry(
            max_attempts=3
        ).next(
            next_step
        )

    def create_step_function_task_with_error_handler(
        self, task_name=None, lambda_function=None, error_handler=None
    ):
        return self.create_stepfunctions_task(
            task_name=task_name,
            lambda_function=lambda_function,
        ).add_catch(
            error_handler,
            result_path=f"$.{task_name}Error"
        )

    def create_lambda_construct(
        self, function_name=None, environment_variables=None,
    ):
        return well_architected_constructs.lambda_function.LambdaFunction(
            self, f'{function_name}Lambda',
            function_name=function_name,
            error_topic=self.error_topic,
            lambda_directory=self.lambda_directory,
            environment_variables=environment_variables,
        )

    def create_bookings_lambda_function(
        self, table: aws_cdk.aws_dynamodb.Table=None,
        function_name=None,
    ):
        lambda_construct = self.create_lambda_construct(
            function_name=function_name,
            environment_variables={
                'TABLE_NAME': table.table_name
            }
        )
        table.grant_read_write_data(lambda_construct.lambda_function)
        return lambda_construct