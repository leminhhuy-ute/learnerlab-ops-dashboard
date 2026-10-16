import json, os
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
ACCOUNT=os.environ['ACCOUNT']
TABLE=boto3.resource('dynamodb').Table(os.environ['TABLE'])
def handler(event, context):
    now=datetime.now(timezone.utc); today=now.date(); stamp=now.strftime('%Y%m%dT%H%M%SZ')
    key={'PK':f'CE#{ACCOUNT}#{today.isoformat()}','SK':'BUDGET'}
    try:
        budget=TABLE.update_item(Key=key,UpdateExpression='SET updatedAt=:now ADD #attempts :one',ConditionExpression='attribute_not_exists(#attempts) OR #attempts < :limit',ExpressionAttributeNames={'#attempts':'attempts'},ExpressionAttributeValues={':now':now.strftime('%Y-%m-%dT%H:%M:%SZ'),':one':1,':limit':4},ReturnValues='UPDATED_NEW')
    except ClientError as error:
        if error.response.get('Error',{}).get('Code')=='ConditionalCheckFailedException': return {'status':'limited','message':'Four Cost Explorer requests already recorded for this UTC day'}
        raise
    attempts=int(budget['Attributes']['attempts']); start=today.replace(day=1).isoformat(); end=(today+timedelta(days=1)).isoformat()
    client=boto3.client('ce',region_name='us-east-1',config=Config(retries={'total_max_attempts':1}))
    try:
        response=client.get_cost_and_usage(TimePeriod={'Start':start,'End':end},Granularity='MONTHLY',Metrics=['UnblendedCost'],GroupBy=[{'Type':'DIMENSION','Key':'SERVICE'}])
        periods=response.get('ResultsByTime',[]); period=periods[0] if periods else {}; groups=[]
        for group in period.get('Groups',[]):
            metric=group.get('Metrics',{}).get('UnblendedCost',{})
            groups.append({'service':group.get('Keys',['Unknown'])[0],'amount':Decimal(str(metric.get('Amount','0'))),'unit':metric.get('Unit','USD')})
        total=sum((g['amount'] for g in groups),Decimal('0'))
        item={'PK':f'BILLING#{ACCOUNT}','SK':f'SNAPSHOT#{stamp}','service':'CostExplorer','periodStart':start,'periodEndExclusive':end,'granularity':'MONTHLY','status':'ok' if periods else 'empty','estimated':bool(period.get('Estimated',True)),'currency':'USD','total':total,'serviceTotals':groups,'requestCountToday':attempts,'collectedAt':stamp}
        TABLE.put_item(Item=item)
        return {'status':item['status'],'snapshotId':stamp,'periodStart':start,'periodEndExclusive':end,'estimated':item['estimated'],'currency':'USD','total':str(total),'serviceGroups':len(groups),'requestCountToday':attempts,'services':[{'service':g['service'],'amount':str(g['amount'])} for g in groups]}
    except ClientError as error:
        code=error.response.get('Error',{}).get('Code','ClientError')
        TABLE.put_item(Item={'PK':f'BILLING#{ACCOUNT}','SK':f'SNAPSHOT#{stamp}','service':'CostExplorer','periodStart':start,'periodEndExclusive':end,'status':'unavailable','errorCode':code,'requestCountToday':attempts,'collectedAt':stamp})
        return {'status':'unavailable','errorCode':code,'requestCountToday':attempts}
