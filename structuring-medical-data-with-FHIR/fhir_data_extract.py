import json
import boto3
import base64
s3 = boto3.client('s3')
'''
This function reads the medical text file written in FHIR format, and returns the data and the data type fhir for downstream processing. 
- Note the code on lines 15–20. You must update these lines of code in the later DIY section.  
'''
def lambda_handler(event, context):

    file_name = event['Key'].split('/')[3]
    s3.download_file(event['Bucket'], event['Key'], f'/tmp/{file_name}')

    # read json file
    file = open(f'/tmp/{file_name}')
    resource = json.load(file)
    
    ################################# WORK ON THE CODE BELOW FOR DIY ###########
    # TODO: Extract clinical notes in document reference
    # Replace TO_BE_PROVIDED with correct key to retrieve based64 encoded clinical notes
    # Remember to place the key name in double quotes

    # data = resource["content"][0]["attachment"][TO_BE_PROVIDED]

    # TODO: Decode data 
    # Replace TO_BE_PROVIDED with correct variable to decode data from based64.

    # decoded_data = base64.b64decode(TO_BE_PROVIDED).decode('utf-8').replace("'",'"')

    return {
        'Notes': decoded_data,
        'Filename': file_name,
        'DataType': 'fhir'
    }
