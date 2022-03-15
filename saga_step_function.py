from aws_cdk import (
    aws_lambda,
    aws_apigateway,
    aws_dynamodb as dynamo_db,
    aws_stepfunctions,
    aws_stepfunctions_tasks,
    core as cdk
)


class SagaStepFunction(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
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
        #
        # 1) Flights
        # 2) Hotel
        # 3) Payment

        # 1) Flights
        reserve_flight = self.alt_create_lambda_function(
            self,
            function_name='flights/reserve_flight',
            table=bookings
        )
        confirm_flight = self.alt_create_lambda_function(
            self,
            function_name='flights/confirmFlight.handler',
            table=bookings
        )
        cancel_flight = self.create_lambda_function(
            scope=self, lambda_id="cancelFlightLambdaHandler",
            handler='flights/cancelFlight.handler', table=bookings
        )

        # 2) Hotel
        reserve_hotel = self.create_lambda_function(scope=self, lambda_id="reserveHotelLambdaHandler",
                                                  handler='hotel/reserveHotel.handler', table=bookings)
        confirm_hotel = self.create_lambda_function(scope=self, lambda_id="confirmHotelLambdaHandler",
                                                  handler='hotel/confirmHotel.handler', table=bookings)
        cancel_hotel = self.create_lambda_function(scope=self, lambda_id="cancelHotelLambdaHandler",
                                                 handler='hotel/cancelHotel.handler', table=bookings)

        # 3) Payment For Holiday
        process_payment = self.create_lambda_function(scope=self, lambda_id="takePaymentLambdaHandler",
                                                 handler='payment/takePayment.handler', table=bookings)
        refund_payment = self.create_lambda_function(scope=self, lambda_id="refundPaymentLambdaHandler",
                                                   handler='payment/refundPayment.handler', table=bookings)

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
            lambda_function=cancel_hotel,
            result_path='$.CancelHotelReservationResult'
        ).add_retry(max_attempts=3).next(booking_failed)

        reserve_hotel = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'ReserveHotel',
            lambda_function=reserve_hotel,
            result_path='$.ReserveHotelResult'
        ).add_catch(cancel_hotel_reservation, result_path="$.ReserveHotelError")

        cancel_flight_reservation = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'CancelFlightReservation',
            lambda_function=cancel_flight,
            result_path='$.CancelFlightReservationResult'
        ).add_retry(max_attempts=3).next(cancel_hotel_reservation)

        reserve_flight = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'ReserveFlight',
            lambda_function=reserve_flight,
            result_path='$.ReserveFlightResult'
        ).add_catch(cancel_flight_reservation, result_path="$.ReserveFlightError")

        # 2) Take Payment
        refund_payment = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'RefundPayment',
            lambda_function=refund_payment,
            result_path='$.RefundPaymentResult'
        ).add_retry(max_attempts=3).next(cancel_flight_reservation)

        take_payment = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'TakePayment',
            lambda_function=process_payment,
            result_path='$.TakePaymentResult'
        ).add_catch(refund_payment, result_path="$.TakePaymentError")

        # 3) Confirm Flight and Hotel Booking
        confirm_hotel = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'ConfirmHotelBooking',
            lambda_function=confirm_hotel,
            result_path='$.ConfirmHotelBookingResult'
        ).add_catch(refund_payment, result_path="$.ConfirmHotelBookingError")

        confirm_flight = aws_stepfunctions_tasks.LambdaInvoke(
            self, 'ConfirmFlight',
            lambda_function=confirm_flight,
            result_path='$.ConfirmFlightResult'
        ).add_catch(refund_payment, result_path="$.ConfirmFlightError")

        definition = aws_stepfunctions.Chain \
            .start(reserve_hotel) \
            .next(reserve_flight) \
            .next(take_payment) \
            .next(confirm_hotel) \
            .next(confirm_flight) \
            .next(booking_succeeded)

        saga = aws_stepfunctions.StateMachine(
            self, 'BookingSaga',
            definition=definition,
            timeout=cdk.Duration.minutes(5)
        )

        # defines an AWS Lambda resource to connect to our API Gateway and kick
        # off our step function
        saga_lambda = aws_lambda.Function(
            self, "sagaLambdaHandler",
            runtime=aws_lambda.Runtime.NODEJS_12_X,
            handler="sagaLambda.handler",
            code=aws_lambda.Code.from_asset("lambda_functions"),
            environment={
                'statemachine_arn': saga.state_machine_arn
            }
        )
        saga.grant_start_execution(saga_lambda)

        # defines an API Gateway REST API resource backed by our "stateMachineLambda" function.
        aws_apigateway.LambdaRestApi(
            self, 'SagaPatternSingleTable',
            handler=saga_lambda
        )

    def create_lambda_function(self, scope: cdk.Stack, lambda_id: str, handler: str, table: dynamo_db.Table):
        function = aws_lambda.Function(
            scope, lambda_id,
            runtime=aws_lambda.Runtime.NODEJS_12_X,
            handler=handler,
            code=aws_lambda.Code.from_asset("lambda_functions"),
            environment={
                'TABLE_NAME': table.table_name
            }
        )
        table.grant_read_write_data(function)
        return function

    def alt_create_lambda_function(self, scope: cdk.Stack, table: dynamo_db.Table=None, function_name=None):
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
