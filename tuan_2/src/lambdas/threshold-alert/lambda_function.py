import json
import os
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ['TABLE_NAME']
TOPIC_ARN = os.environ['TOPIC_ARN']
ACCOUNT_ID = os.environ['ACCOUNT_ID']
THRESHOLD = Decimal(os.environ.get('ALERT_THRESHOLD_USD', '10'))
REGION = os.environ.get('AWS_REGION', 'us-east-1')

ddb = boto3.resource('dynamodb', region_name=REGION).Table(TABLE_NAME)
sns = boto3.client('sns', region_name=REGION)

def lambda_handler(event, context):
    event = event or {}
    if event.get('test') is True:
        result = sns.publish(
            TopicArn=TOPIC_ARN,
            Subject='Learner Lab SNS integration test',
            Message='SNS integration test for learnerlab-ops-week2-alerts. This is not a cost alert.'
        )
        return {'status': 'sns_test_published', 'messageId': result['MessageId']}

    response = ddb.query(
        KeyConditionExpression=Key('PK').eq('BILLING#' + ACCOUNT_ID),
        ScanIndexForward=False,
        Limit=1
    )
    items = response.get('Items', [])
    if not items:
        return {'status': 'no_billing_snapshot', 'published': False}

    item = items[0]
    if item.get('status') != 'ok':
        return {'status': 'billing_snapshot_not_ok', 'published': False,
                'snapshotId': item.get('SK')}

    amount = Decimal(str(item.get('total', '0')))
    details = {
        'periodStart': item.get('periodStart'),
        'periodEndExclusive': item.get('periodEndExclusive'),
        'estimated': bool(item.get('estimated', True)),
        'amountUsd': str(amount),
        'thresholdUsd': str(THRESHOLD),
        'snapshotId': item.get('SK')
    }
    if amount < THRESHOLD:
        return {'status': 'below_threshold', 'published': False, **details}

    result = sns.publish(
        TopicArn=TOPIC_ARN,
        Subject='Learner Lab estimated cost threshold reached',
        Message=json.dumps(details, ensure_ascii=False)
    )
    return {'status': 'alert_published', 'published': True,
            'messageId': result['MessageId'], **details}
