import boto3
import os
import random

TABLE = boto3.resource('dynamodb').Table(os.environ.get('TABLE_NAME'))

def handler(event, context):
    print(f"request: {event}")
    
    pass

Object.defineProperty(exports, "__esModule", { value: true });

exports.handler = async function (event) {
    if (Math.random() < 0.4) {
        throw new Error("Internal Server Error");
    }
    let bookingID = '';
    if (typeof event.ReserveFlightResult !== 'undefined') {
        bookingID = event.ReserveFlightResult.Payload.booking_id;
    }
    // create AWS SDK clients
    const dynamo = new DynamoDB();
    var params = {
        TableName: process.env.TABLE_NAME,
        Key: {
            'pk': { S: event.trip_id },
            'sk': { S: 'FLIGHT#' + bookingID }
        }
    };
    // Call DynamoDB to add the item to the table
    let result = await dynamo.deleteItem(params).promise().catch((error) => {
        throw new Error(error);
    });
    console.log('deleted flight booking:');
    console.log(result);
    // return status of ok
    return { status: "ok" };
};