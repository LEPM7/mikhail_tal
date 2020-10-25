import os
import json
import boto3
from urllib.parse import parse_qs

import sys
sys.path.insert(0, 'lambdas/')

def get_emergency(event, context):
    REGION                  = os.environ["AWS_REGION"]
    DYNAMODB_TABLE          = os.environ["DYNAMODB_TABLE"]
    
    dynamodb = boto3.resource('dynamodb',region_name=REGION)
    table = dynamodb.Table(DYNAMODB_TABLE)
    items = []
    for item in table.scan()["Items"]:
        dict = {}
        dict["id"]=str(item["id"])
        dict["latitude"]=str(item["latitude"])
        dict["longitude"]=str(item["longitude"])
        dict["fireStation"]=str(item["fireStation"])
        dict["contactPhone"]=str(item["contactPhone"])
        dict["ambulance"]=str(item["ambulance"])
        dict["state"]=str(item["state"])
        items.append(dict)

    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }

# LOCAL TESTING
# export AWS_REGION=us-east-1
# export AWS_PROFILE=trambo
# export DYNAMODB_TABLE=Emergency
# print(get_emergency({"postBody" : "test"},""))
