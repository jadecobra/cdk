import aws_cdk
import constructs
import well_architected
import well_architected_lambda
import well_architected_dynamodb_table

from aws_cdk import (
    aws_lambda,
    aws_apigateway,
    aws_dynamodb as dynamo_db,
    aws_stepfunctions,
    aws_stepfunctions_tasks,
)


class SagaStepFunction(well_architected.WellArchitectedStack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bookings = well_architected_dynamodb_table.DynamoDBTableConstruct(
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
        cancel_hotel_reservation = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'CancelHotelReservation',
            lambda_function=hotel_cancellation_function,
            result_path='$.CancelHotelReservationResult'
        ).add_retry(
            max_attempts=3
        ).next(
            aws_stepfunctions.Fail(self, "Sorry, We Couldn't make the booking")
        )

        reserve_hotel = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'ReserveHotel',
            lambda_function=hotel_reservation_function,
            result_path='$.ReserveHotelResult'
        ).add_catch(cancel_hotel_reservation, result_path="$.ReserveHotelError")

        cancel_flight_reservation = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'CancelFlightReservation',
            lambda_function=flight_cancellation_function,
            result_path='$.CancelFlightReservationResult'
        ).add_retry(max_attempts=3).next(cancel_hotel_reservation)

        reserve_flight = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'ReserveFlight',
            lambda_function=flight_reservation_function,
            result_path='$.ReserveFlightResult'
        ).add_catch(cancel_flight_reservation, result_path="$.ReserveFlightError")

        # 2) Take Payment
        refund_payment = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'RefundPayment',
            lambda_function=payment_refund_function,
            result_path='$.RefundPaymentResult'
        ).add_retry(max_attempts=3).next(cancel_flight_reservation)

        process_payment = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'TakePayment',
            lambda_function=payment_processing_function,
            result_path='$.TakePaymentResult'
        ).add_catch(refund_payment, result_path="$.TakePaymentError")

        # 3) Confirm Flight and Hotel Booking
        confirm_hotel = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'ConfirmHotelBooking',
            lambda_function=hotel_confirmation_function,
            result_path='$.ConfirmHotelBookingResult'
        ).add_catch(refund_payment, result_path="$.ConfirmHotelBookingError")

        confirm_flight = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'ConfirmFlight',
            lambda_function=flight_confirmation_function,
            result_path='$.ConfirmFlightResult'
        ).add_catch(refund_payment, result_path="$.ConfirmFlightError")

        saga_state_machine = aws_stepfunctions.StateMachine(
            self, 'BookingSaga',
            definition=(
                aws_stepfunctions
                    .Chain
                    .start(reserve_hotel)
                    .next(reserve_flight)
                    .next(process_payment)
                    .next(confirm_hotel)
                    .next(confirm_flight)
                    .next(aws_stepfunctions.Succeed(self, 'We have made your booking!'))
            ),
            timeout=aws_cdk.Duration.minutes(5)
        )

        saga_lambda = well_architected_lambda.LambdaFunctionConstruct(
            self, 'SagaLambda',
            error_topic=self.error_topic,
            function_name='saga_lambda',
            environment_variables={
                'statemachine_arn': saga_state_machine.state_machine_arn
            },
        ).lambda_function

        saga_state_machine.grant_start_execution(saga_lambda)

        aws_apigateway.LambdaRestApi(
            self, 'SagaPatternSingleTable',
            handler=saga_lambda
        )

    def create_lambda_function(self, scope: aws_cdk.Stack, table: dynamo_db.Table=None, function_name=None, error_topic=None):
        function = well_architected_lambda.LambdaFunctionConstruct(
            self, function_name,
            function_name=function_name,
            error_topic=error_topic,
            environment_variables={
                'TABLE_NAME': table.table_name
            }
        ).lambda_function
        # function = aws_lambda.Function(
        #     scope, function_name,
        #     runtime=aws_lambda.Runtime.PYTHON_3_9,
        #     handler=f'{function_name}.handler',
        #     code=aws_lambda.Code.from_asset(f"lambda_functions/{function_name}"),
        #     environment={
        #         'TABLE_NAME': table.table_name
        #     }
        # )
        table.grant_read_write_data(function)
        return function