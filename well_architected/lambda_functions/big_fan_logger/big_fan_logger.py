import json
import logging

def handler(event, context):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info("request: " + json.dumps(event))

    for record in event["Records"]:
        payload = record["body"]
        logger.info("received message " + payload)