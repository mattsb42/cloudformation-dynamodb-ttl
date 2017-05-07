"""
Cloudformation custom resource provider for DynamoDB TTL.

Properties format: {
    "TableName": <table name>,
    "TimeToLiveSpecification": {
        "Enabled": <bool>,
        "AttributeName": <ttl attribute name>
    }
}
"""
import json
import logging

import boto3
import cfnresponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
_is_setup = False


def _setup():
    """Creates long-lived clients to reduce warm-start startup times."""
    global ddb
    ddb = boto3.client('dynamodb')
    global _is_setup
    _is_setup = True


def _set_ttl(event):
    """Makes DynamoDB update TTL call based on event.

    :param dict event: Lambda Event object
    """
    ddb.update_time_to_live(
        TableName=event['ResourceProperties']['TableName'],
        TimeToLiveSpecification=dict(
            Enabled=event['ResourceProperties']['TimeToLiveSpecification']['Enabled'],
            AttributeName=event['ResourceProperties']['TimeToLiveSpecification']['AttributeName']
        )
    )


def lambda_handler(event, context):
    """Lambda handler function.

    :param dict event: Lambda Event object
    :param context: Lambda Context object
    """
    logger.info(json.dumps(event))
    if not _is_setup:
        _setup()
    try:
        if event['RequestType'] in ('Create', 'Update'):
            _set_ttl(event)
    except Exception:
        logger.exception('Unexpected exception performing action: %s', event['RequestType'])
        cfnresponse.send(
            event=event,
            context=context,
            response_status=cfnresponse.FAILED,
            physical_resource_id=event.get('PhysicalResourceId', None)
        )
    else:
        cfnresponse.send(
            event=event,
            context=context,
            response_status=cfnresponse.SUCCESS,
            reason=None,
            reaponse_data={'AttributeName': event['ResourceProperties']['TimeToLiveSpecification']['AttributeName']},
            physical_resource_id=event.get('PhysicalResourceId', None)
        )
