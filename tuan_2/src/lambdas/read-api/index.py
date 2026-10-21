import json, os
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key
TABLE=boto3.resource('dynamodb').Table(os.environ['TABLE'])
ACCOUNT=os.environ['ACCOUNT']
REGIONS=json.loads(os.environ['REGIONS'])
SERVICES=['EC2','RDS','SAGEMAKER_ENDPOINT','SAGEMAKER_NOTEBOOK','EKS']
def latest(pk):
    result=TABLE.query(KeyConditionExpression=Key('PK').eq(pk) & Key('SK').begins_with('SNAPSHOT#'),ScanIndexForward=False,Limit=1)
    return (result.get('Items') or [None])[0]
def handler(event, context):
    inventory=[]
    for region in REGIONS:
        for service in SERVICES:
            item=latest(f'INVENTORY#{service}#{region}')
            inventory.append({'service':service,'region':region,'status':item.get('status') if item else 'missing','count':item.get('count') if item else None,'collectedAt':item.get('collectedAt') if item else None,'errorCode':item.get('errorCode') if item else None})
    bill=latest(f'BILLING#{ACCOUNT}')
    billing={'status':bill.get('status') if bill else 'missing'}
    if bill:
        billing.update({'periodStart':bill.get('periodStart'),'periodEndExclusive':bill.get('periodEndExclusive'),'estimated':bill.get('estimated'),'currency':bill.get('currency'),'total':str(bill['total']) if isinstance(bill.get('total'),Decimal) else bill.get('total'),'serviceGroups':len(bill.get('serviceTotals',[])),'requestCountToday':bill.get('requestCountToday')})
    overall='ok' if all(x['status']=='ok' for x in inventory) and billing.get('status')=='ok' else 'partial'
    return {'status':overall,'inventory':inventory,'billing':billing}
