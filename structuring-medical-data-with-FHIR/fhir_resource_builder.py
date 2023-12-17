import json
import boto3 
import os
import base64
import time
import datetime


'''
This function search for patient records in DynamoDB table, and insert medical entities (detected by Comprehend Medical) to the patient records.
'''
table_name = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)
s3 = boto3.client('s3')

def docref_template(cm_output, uuid):
    # define a datetime
    current_time = datetime.datetime.now()
    interval = datetime.timedelta(minutes = 15)
    final_time = current_time+interval
    transcriptionTime = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    encounterStartTime = transcriptionTime
    encounterEndTime = final_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    serviceProvider = 'serviceProvider'
    serviceProviderDisplay = 'serviceProviderDisplay'
    
    #FHIR documentReference store data in base64 encode
    encoded_cm_output = base64. \
        b64encode(str(cm_output).encode('ascii') ). \
        decode('utf-8')

    jsonDocRefTemplate = {
      "fullUrl": f"urn:uuid:{uuid}",
      "resource": {
            "resourceType":"DocumentReference",
            "date": transcriptionTime,
            "custodian":{
               "reference": serviceProvider,
               "display": serviceProviderDisplay
            },
            "subject":{
               "reference":"subject"
            },
            "author":[
               {
                  "reference":"practID",
                  "display":"practDisplay"
               }
            ],
            "context":{
               "period":{
                  "start": encounterStartTime,
                  "end": encounterEndTime
               },
               "encounter":[
                  {
                     "reference":"idEncounter"
                  }
               ]
            },
            "type":{
               "coding":[
                  {
                     "system":"http://loinc.org",
                     "code":"75519-9",
                     "display":"Encounter"
                  }
               ]
            },
            "category":[
               {
                  "coding":[
                     {
                        "system":"http://hl7.org/fhir/us/core/CodeSystem/us-core-documentreference-category",
                        "code":"clinical-note",
                        "display":"Clinical Note"
                     }
                  ]
               }
            ],
            "content":[
               {
                  "attachment":{
                     "data": encoded_cm_output,
                     "contentType":"text/plain"
                  }
               }
            ],
            "status":"superseded"
      },
      "request": {
        "method": "POST",
        "url": "DocumentReference"
      }
    }
    return jsonDocRefTemplate
        
def generate_docref_for_hl7(data, cm_output):
    
    #random UUID for the DocumentReference
    uuid = '4a01f6c8-5f3a-4122-80ab-405312f96aa2'
    search_docref_resource = any(d.get("resource",{}).get("resourceType") == "DocumentReference" for d in data['entry'])

    if search_docref_resource:
        return None
    else:
        new_docref = docref_template(cm_output,uuid)
        
        #add new DocumentReference to data
        data['entry'].append(new_docref)
        return data
        
def linkage_template(source_uuid,alternate_uuid):

    #Create a linkage to map relationship between new and old DocumentReference
    linkage_uuid = '394bb244-177b-4409-8657-27951edce5c7'
    
    current_time = datetime.datetime.now()
    transcriptionTime = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    jsonLinkageTemplate = {
		"resourceType": "Linkage",
		"id": linkage_uuid,
		"active": "true",
		"item": [
			{
				"type": "alternate",
				"resource": {
					"reference": f"DocumentReference/{alternate_uuid}",
					"type": "DocumentReference"
				}
			},
			{
				"type": "source",
				"resource": {
					"reference": f"DocumentReference/{source_uuid}",
					"type": "DocumentReference"
				}
			}
		],
		"meta": {
			"lastUpdated": transcriptionTime,
			"tag": [{
				"display": "SYSTEM_GENERATED"
			}]
        }
    }
    return jsonLinkageTemplate

def lambda_handler(event, context):
    
    dataType = event['DataType']
    cm_output_bucket = event['CMOutputBucket']
    file_name = event['CMOutputKey'].split('/')[2]

    s3.download_file(event['CMOutputBucket'], event['CMOutputKey'], f'/tmp/{file_name}')
    
    cm_file = open(f'/tmp/{file_name}')
    cm_output_result = json.load(cm_file)
    
    if dataType == 'hl7':
        try:
            query_hl7_item = table.get_item(Key={'resource_id': '1', 'type': 'Bundle'})
            hl7_data = json.loads(query_hl7_item['Item']['resource'])
            
            #generate a DocumentReference and append to data.
            updated_hl7_data = generate_docref_for_hl7(hl7_data,cm_output_result)
            
            #Update the data in DynamoDB
            if updated_hl7_data is not None:
                try: 
                    put_new_data = table.update_item(
                        Key={
                            'resource_id': '1',
                            'type': 'Bundle'
                        },
                        UpdateExpression="set #resource=:r",
                        ExpressionAttributeNames={
                            '#resource': 'resource'
                        },
                        ExpressionAttributeValues={
                            ':r': json.dumps(updated_hl7_data)
                        },
                        
                        ReturnValues="UPDATED_NEW"
                    )
                except Exception as e:
                    print(e)
 
        except Exception as e:
            print(e)
    
    if dataType == 'fhir':
        try:
            query_fhir_item = table.get_item(Key={'resource_id': '2', 'type': 'DocumentReference'})
            fhir_data = json.loads(query_fhir_item['Item']['resource'])
            
            source_uuid = fhir_data['id']
            alternate_uuid = 'fbfb77d8-70cf-4579-9926-27951edce5c7'

            # generate a new DocumentReference to store the output from Comprehend Medical
            new_docref = docref_template(cm_output_result,alternate_uuid)

            #create a linkage to link old and new DocumentReference
            new_linkage = linkage_template(source_uuid,alternate_uuid)
            
            # put new document and linkage to DynamoDB table
            try:
                put_new_docref = table.put_item(
                    Item={
                        'resource_id': '3',
                        'type': 'DocumentReference',
                        'resource': json.dumps(new_docref)
                    }
                )
            except Exception as e:
                print(e)
                
            try:
                put_new_linkage = table.put_item(
                    Item={
                        'resource_id': '4',
                        'type': 'Linkage',
                        'resource': json.dumps(new_linkage)
                    }
                )
            except Exception as e:
                print(e)            
        except Exception as e:
            print(e)
