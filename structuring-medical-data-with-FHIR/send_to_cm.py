import json
import boto3 
import os
'''
his function sends the medical data to Amazon Comprehend Medical and stores the results in an S3 bucket. 
'''
comprehend = boto3.client(service_name='comprehendmedical')
s3 = boto3.client('s3')

output_bucket = os.environ["OUTPUT_BUCKET"]
hl7_file_path = os.environ["HL7_OUTPUT_PATH"]
fhir_file_path = os.environ["FHIR_OUTPUT_PATH"]

def lambda_handler(event, context):
    
    data_type = event['DataType']
    file_name = event['Filename']
    notes = event['Notes']
    
    result = comprehend.detect_entities(Text=notes)
    
    response={}
    if data_type == 'hl7':
        s3.put_object(Body=json.dumps(result,indent=2), Bucket=output_bucket, Key=f'{hl7_file_path}/{file_name}')
        response = {
            'CMOutputBucket': output_bucket,
            'CMOutputKey': f"{hl7_file_path}/{file_name}",
            'DataType':data_type
        } 
    if data_type == 'fhir':
        s3.put_object(Body=json.dumps(result,indent=2), Bucket=output_bucket, Key=f'{fhir_file_path}/{file_name}')
        response = {
            'CMOutputBucket': output_bucket,
            'CMOutputKey': f"{fhir_file_path}/{file_name}",
            'DataType':data_type
        } 
        
    return response