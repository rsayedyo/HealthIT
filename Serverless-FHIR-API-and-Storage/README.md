# Serverless FHIR API And Storage


## Objectives

Hospital would like to implement a software toolkit to give external developers the ability to add serverless FHIR APIs to their own applications. In addition, the hospital wants to connect their healthcare applications to others. The solution needs to be able to perform the Create, Read, Update, and Delete (CRUD) operations for all R4 or STU3 base FHIR resources, and must provide search capabilities by resource type.


### Targeted KPI
- Increase overall patient satisfaction
- Improve emergency room wait times
- Improve average patient wait times

## HLD
In this solution, a healthcare application AWS lambda function has its APIs exposed to external developers through Amazon API Gateway.

## LLD

- When the external application creates a record through the API, the request is forwarded to the fhir_curd lambda function, and the data is saved to an Amazon DynamoDB table.

- After the record is written to a DynamoDB table, fhir_replication function replicates the data into Amazon OpenSearchService

- When the application requests data from a record, API Geteway forwards the requests to fhir_curd lambda functions
  - Simple requests are returned from the DynamoDB
  - More complex queries, attributes, or other requests are sent to OpenSearchService

- After the data from DyanmoDB or OpenSearch is returned to the fhir_curd function, it is forwarded back to the requesting application.
