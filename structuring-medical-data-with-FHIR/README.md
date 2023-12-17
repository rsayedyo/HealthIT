# Structuring Medical Data with FHIR


## Objectives

Hospital would like to better orgranize the receipt of EHR, using a modern method to store the files and extract the unstructured medical data frmo them.

### Targeted KPI
- Increase overall patient satisfaction
- Increase profit margins
- Improve average patient wait times

## HLD
In this solution, a serverless workflow is created using AWS step function and AWS Lambda functions to extract medical entities from unstructured documents and store them, meeting the FHIR standards.

## LLD

- The step function's state machine (workflow starts when a clinical note is uploaded to S3 bucket
    - The s3 upload trigger invokes a lambda functions which invokes the state machine to start the workflow.

- First, the state machine invokes the lambda function 'HealthDataRouter.py'.
    - This function reads the file from S3 and determines if the the file is currently in HL7 or FHIR format

- If the file is not in FHIR or HL7 format the state machine will fail

- If the raw data is in HL7 format, the state machine invokes the lambda function 'HL7DataExtractFunction.py' to parse the Data

- If the raw data is in FHIR format,  the state machine invokes the lambda function 'FHIRDataExtractFunction.py' to parse the data

- Parsed data is sent to lambda function 'SendToCMFunction.py'. This function sends API calls to Amazon Comprehend Medical to detect medical entities.

- The detected medical entities are written into JSON format and stored on an S3 bucket by Amazon Comprehend Medical

- Finally, the state machine invokes 'FHIRResourceBuilder.py' to read the medical entities from the JSON file on the S3 bucket.
    - The FHIRResourceBuilder.py function queries the FHIR data store table in Amazon Dynamo DB to retrieve patient information.
    - The FHIRResourceBuilder.py function then inserts detected medical entities into the patient information, now an updated patient record in the data store.
