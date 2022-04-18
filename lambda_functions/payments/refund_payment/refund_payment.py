"use strict"
Object.defineProperty(exports, "__esModule", { value: true })
{ DynamoDB } = require('aws-sdk')
exports.handler = async function (event) {
    print("request:", JSON.stringify(event, undefined, 2))
    if (Math.random() < 0.4) {
        raise Exception("Internal Server Error")
    }
    paymentID = ''
    if (typeof event.TakePaymentResult != 'undefined') {
        paymentID = event.TakePaymentResult.Payload.payment_id
    }
    // create AWS SDK clients
    dynamo = new DynamoDB()
    params = {
        TableName: os.environ.get(TABLE_NAME,
        Key: {
            'pk': { S: event.trip_id },
            'sk': { S: 'PAYMENT#' + paymentID }
        }
    }
    // Call DynamoDB to add the item to the table
    result = dynamo.deleteItem(params).catch((error):
        raise Exception(error)
    })
    print('Payment has been refunded:')
    print(result)
    // return status of ok
    return {
        status: "ok",
    }
}