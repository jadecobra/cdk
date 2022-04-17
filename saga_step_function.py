import aws_cdk
import constructs

from aws_cdk import (
    aws_lambda,
    aws_apigateway,
    aws_dynamodb as dynamo_db,
    aws_stepfunctions,
    aws_stepfunctions_tasks,
)


class SagaStepFunction(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bookings = dynamo_db.Table(
            self, "Bookings",
            partition_key=dynamo_db.Attribute(name="booking_id", type=dynamo_db.AttributeType.STRING),
            sort_key=dynamo_db.Attribute(name="booking_type", type=dynamo_db.AttributeType.STRING)
        )

        ###
        # Lambda Functions
        ###
        # We need Booking and Cancellation functions for our 3 services
        #
        # All functions need access to our DynamoDB table above.
        # We also need to take payment for this trip

        flight_reservation_function = self.create_lambda_function(
            self,
            function_name='flights/reserve_flight',
            table=bookings
        )
        flight_confirmation_function = self.create_lambda_function(
            self,
            function_name='flights/confirm_flight',
            table=bookings
        )
        flight_cancellation_function = self.create_lambda_function(
            self,
            function_name='flights/cancel_flight',
            table=bookings
        )

        hotel_reservation_function = self.create_lambda_function(
            self,
            function_name="hotels/reserve_hotel",
            table=bookings
        )

        hotel_confirmation_function = self.create_lambda_function(
            self,
            function_name='hotels/confirm_hotel',
            table=bookings
        )

        hotel_cancellation_function = self.create_lambda_function(
            self,
            function_name="hotels/cancel_hotel",
            table=bookings
        )

        payment_processing_function = self.create_lambda_function(
            self,
            function_name="payments/process_payment",
            table=bookings
        )

        payment_refund_function = self.create_lambda_function(
            self,
            function_name="payments/refund_payment",
            table=bookings
        )

        ###
        # Saga Pattern Step Function
        ###
        # Follows a strict order:
        # 1) Reserve Flights and Hotel
        # 2) Take Payment
        # 3) Confirm Flight and Hotel booking

        # Our two end states
        booking_succeeded = aws_stepfunctions.Succeed(self, 'We have made your booking!')
        booking_failed = aws_stepfunctions.Fail(self, "Sorry, We Couldn't make the booking")

        # 1) Reserve Flights and Hotel
        cancel_hotel_reservation = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'CancelHotelReservation',
            lambda_function=hotel_cancellation_function,
            result_path='$.CancelHotelReservationResult'
        ).add_retry(max_attempts=3).next(booking_failed)

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
                aws_stepfunctions.Chain
                                .start(reserve_hotel)
                                .next(reserve_flight)
                                .next(process_payment)
                                .next(confirm_hotel)
                                .next(confirm_flight)
                                .next(booking_succeeded)
            ),
            timeout=cdk.Duration.minutes(5)
        )

        saga_lambda = aws_lambda.Function(
            self, "sagaLambdaHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="saga_lambda.handler",
            code=aws_lambda.Code.from_asset("lambda_functions/saga_lambda"),
            environment={
                'statemachine_arn': saga_state_machine.state_machine_arn
            }
        )
        saga_state_machine.grant_start_execution(saga_lambda)

        aws_apigateway.LambdaRestApi(
            self, 'SagaPatternSingleTable',
            handler=saga_lambda
        )

    def create_lambda_function(self, scope: cdk.Stack, table: dynamo_db.Table=None, function_name=None):
        function = aws_lambda.Function(
            scope, function_name,
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler=f'{function_name}.handler',
            code=aws_lambda.Code.from_asset(f"lambda_functions/{function_name}"),
            environment={
                'TABLE_NAME': table.table_name
            }
        )
        table.grant_read_write_data(function)
        return function