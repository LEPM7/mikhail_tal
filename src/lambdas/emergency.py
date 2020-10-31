import os
import json
import boto3
from boto3.dynamodb.conditions import Key

def get_all_emergency(event, context):
    REGION                  = os.environ["AWS_REGION"]
    DYNAMODB_TABLE          = os.environ["DYNAMODB_TABLE"]
    dynamodb = boto3.resource('dynamodb',region_name=REGION)
    table = dynamodb.Table(DYNAMODB_TABLE)
    return table.scan()["Items"]

def get_emergency_by_status(event, context):
    REGION                  = os.environ["AWS_REGION"]
    DYNAMODB_TABLE          = os.environ["DYNAMODB_TABLE"]
    dynamodb = boto3.resource('dynamodb',region_name=REGION)
    table = dynamodb.Table(DYNAMODB_TABLE)
    status= str(event["path"]["status"])
    return table.query(
        Select='ALL_ATTRIBUTES',
        Limit=100,
        ConsistentRead=True,
        ReturnConsumedCapacity='NONE',
        KeyConditionExpression=Key('state').eq(status)
    )["Items"]

def get_emergency_by_id(event, context):
    REGION                  = os.environ["AWS_REGION"]
    DYNAMODB_TABLE          = os.environ["DYNAMODB_TABLE"]
    dynamodb = boto3.resource('dynamodb',region_name=REGION)
    table = dynamodb.Table(DYNAMODB_TABLE)
    id= str(event["path"]["id"])
    print(id)
    return table.query(
        Select='ALL_ATTRIBUTES',
        Limit=100,
        ConsistentRead=True,
        ReturnConsumedCapacity='NONE',
        KeyConditionExpression=Key('state').eq("PENDING") & Key('id').eq(int(id)) 
    )["Items"][0]

def add_emergency(event, context):
    REGION                  = os.environ["AWS_REGION"]
    DYNAMODB_TABLE          = os.environ["DYNAMODB_TABLE"]
    dynamodb = boto3.client('dynamodb',region_name=REGION)
    return dynamodb.put_item(
        TableName=DYNAMODB_TABLE,
        Item={
            'state': {
                'S': 'PENDING'
            },
            'id': {
                'N': str(10)
            }
        }
    )

# LOCAL TESTING
# export AWS_REGION=us-east-1
# export AWS_PROFILE=trambo
# export DYNAMODB_TABLE=Emergency
# print(get_emergency_by_status({"postBody" : "test"},""))
