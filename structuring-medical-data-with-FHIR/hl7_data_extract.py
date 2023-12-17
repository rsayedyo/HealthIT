import json
import boto3
import hl7 
s3 = boto3.client('s3')


'''
This function parses the medical text file written in HL7 format, using the Python library HL7, and returns the parsed data and the data type hl7 for downstream processing
'''

def lambda_handler(event, context):
    filename = event['Key'].split('/')[3]
    s3.download_file(event['Bucket'], event['Key'], f'/tmp/{filename}')

    # read json file
    message = ""
    with open(f'/tmp/{filename}') as document:
        for line in document.readlines():
            message = message  + line + '\r'
    print(message)
    decoded_message = hl7.parse(message)
    raw_data = decoded_message.segments('OBX')
    notes = ""
    for line in raw_data:
        notes = notes + line[5][0] + " "
       
    return {
        'Notes': notes,
        'Filename': filename,
        'DataType': 'hl7'
    }
