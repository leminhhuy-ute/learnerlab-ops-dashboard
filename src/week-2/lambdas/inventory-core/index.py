import json, os
from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError

REGIONS = json.loads(os.environ['REGIONS'])
TABLE = boto3.resource('dynamodb').Table(os.environ['TABLE'])
SESSION = boto3.Session()

def pages(client, operation, key):
    output = []
    paginator = client.get_paginator(operation)
    for page in paginator.paginate():
        output.extend(page.get(key, []))
    return output

def collect(name, region):
    client = SESSION.client({'EC2':'ec2','RDS':'rds','SAGEMAKER_ENDPOINT':'sagemaker','SAGEMAKER_NOTEBOOK':'sagemaker','EKS':'eks'}[name], region_name=region)
    if name == 'EC2':
        reservations = pages(client, 'describe_instances', 'Reservations')
        rows = []
        for reservation in reservations:
            for item in reservation.get('Instances', []):
                rows.append({'id':item.get('InstanceId'), 'state':item.get('State',{}).get('Name'), 'type':item.get('InstanceType'), 'tags':item.get('Tags',[])})
    elif name == 'RDS':
        rows = [{'id':x.get('DBInstanceIdentifier'), 'status':x.get('DBInstanceStatus'), 'engine':x.get('Engine'), 'class':x.get('DBInstanceClass'), 'multiAZ':x.get('MultiAZ')} for x in pages(client, 'describe_db_instances', 'DBInstances')]
    elif name == 'SAGEMAKER_ENDPOINT':
        rows = [{'name':x.get('EndpointName'), 'status':x.get('EndpointStatus'), 'createdAt':x.get('CreationTime').isoformat() if x.get('CreationTime') else None} for x in pages(client, 'list_endpoints', 'Endpoints')]
    elif name == 'SAGEMAKER_NOTEBOOK':
        rows = [{'name':x.get('NotebookInstanceName'), 'status':x.get('NotebookInstanceStatus'), 'type':x.get('InstanceType')} for x in pages(client, 'list_notebook_instances', 'NotebookInstances')]
    else:
        rows = [{'name':x} for x in pages(client, 'list_clusters', 'clusters')]
    return {'status':'ok', 'count':len(rows), 'resources':rows}

def handler(event, context):
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    results = []
    for region in REGIONS:
        for name in ('EC2','RDS','SAGEMAKER_ENDPOINT','SAGEMAKER_NOTEBOOK','EKS'):
            try:
                result = collect(name, region)
            except ClientError as error:
                code = error.response.get('Error',{}).get('Code','ClientError')
                result = {'status':'unavailable' if 'AccessDenied' in code or code == 'UnauthorizedOperation' else 'error', 'count':None, 'resources':[], 'errorCode':code}
            except Exception as error:
                result = {'status':'error', 'count':None, 'resources':[], 'errorCode':type(error).__name__}
            item = {'PK':f'INVENTORY#{name}#{region}', 'SK':f'SNAPSHOT#{timestamp}', 'service':name, 'region':region, 'collectedAt':timestamp, **result}
            TABLE.put_item(Item=item)
            results.append({'service':name,'region':region,'status':result['status'],'count':result['count'],'errorCode':result.get('errorCode')})
    return {'snapshotId':timestamp, 'results':results}
