import json
import urllib.parse
import boto3
import os

'''
- When a new medical text file is uploaded to the S3 bucket, input-bucket-xyz, an S3 event notification invokes this Lambda function.
- Using Boto3, this function starts the state machine, ExtractMedicalData, that you created in earlier steps.
- The state machine ARN is stored in a Lambda function environment variable. 
'''
s3 = boto3.client('s3')
stf = boto3.client('stepfunctions')

state_machine = os.environ['STATE_MACHINE_ARN']

def lambda_handler(event, context):
    print(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    stf_input = {
        'bucket': bucket,
        'key': key
    }
    try:
        stf_response = stf.start_execution(
                            stateMachineArn=state_machine,
                            input=json.dumps(stf_input)
                            )
        print('Started state machine {} '.format(stf_response['executionArn']))

    except Exception as e:
        print(e)
        raise e
