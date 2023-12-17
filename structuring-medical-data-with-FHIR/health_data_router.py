import json
import boto3 

s3 = boto3.client('s3')
'''
This function parses the S3 object key of the medical text file that you upload in a later step
'''
def lambda_handler(event, context):
    print(event)
    #process s3 event notification
    bucket = event['bucket']
    key = event['key']
    key_path = key.split('/')
    if len(key_path) >= 3:
        if key_path[2] != 0:
            data_type = key_path[2]
            print(f'found data type: {data_type} for file {key}')
    
    return {
        'Bucket': bucket,
        'Key': key,
        'DataType': data_type
        }
 