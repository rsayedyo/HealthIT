'''
The fhir_crud function conducts the following operations behind the API: create, read, update, and delete (CRUD)
'''

import base64
import boto3
import json
import requests
from requests_aws4auth import AWS4Auth
from datetime import datetime
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
import os

service = 'es'
credentials = boto3.Session().get_credentials()
dynamodb_client = boto3.client('dynamodb')
session = boto3.session.Session()
region = session.region_name
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

headers = { "Content-Type": "application/json" }

host = os.environ['host']
index = os.environ['index']

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    for record in event['Records']:
        try:
            eventName = record['eventName']
            # PUT sample-index/_doc/1
            if eventName == 'INSERT':
                document = dynamo_obj_to_python_obj(record['dynamodb']['NewImage'])
                id = document['id']
                url = host + '/' + index + '/' + '_doc' + '/' + id
                responsedata = requests.put(url + id, auth=awsauth, json=document, headers=headers)
            # POST /sample-index1/_update/1
            if eventName == 'MODIFY':
                document = dynamo_obj_to_python_obj(record['dynamodb']['NewImage'])
                id = document['id']
                url = host + '/' + index + '/' + '_update' + '/' + id
                new_document = {"doc":document}
                responsedata = requests.post(url + id, auth=awsauth, json=new_document, headers=headers)
            # DELETE /sample-index1/_doc/1
            elif eventName == 'REMOVE':
                document = dynamo_obj_to_python_obj(record['dynamodb']['OldImage'])
                id = document['id']
                url = host + '/' + index + '/' + '_doc' + '/' + id
                responsedata = requests.delete(url + id, auth=awsauth, json=document, headers=headers)

        except Exception as e:
            print(e)

    return 'Successfully processed {} records.'.format(len(event['Records']))

def dynamo_obj_to_python_obj(dynamo_obj: dict) -> dict:
    deserializer = TypeDeserializer()
    return {
        k: deserializer.deserialize(v)
        for k, v in dynamo_obj.items()
    }e
