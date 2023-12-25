# Beds Occupancy Dashboard and Forecast

## Objectives

Hospital would like to create a real-time, visual dashboard that shows bed occupancy and forecasts needs. The data comes from various systems, maintaining a maximum 60-second delay. The solution detect anomalies in out-of-service beds to enable alerts.


### Targeted KPI
- Increase overall patient satisfaction
- Improve emergency room wait times
- Improve average patient wait times
- Improve medical equipment utilization

## HLD
In this solution, hospital bed occupancy can be monitored and managed in realtime by using Amazon Kinesis and Amazon OpenSearch services. Staff can detect anomalies create dashboards and optimize medical equipments and resources allocation.

![open_search_dashboard](https://github.com/rsayedyo/HealthIT/assets/36279070/6fb903b1-c017-45e4-b719-21165000b0a4)


## LLD
- Bed occupancy data is generated and sent to Amazon Kinesis Data Streams by different systems, such as hospital admissions, patient monitoring, and other systems that capture data related to bed occupancy.
  - An Apache Flink Java application is provided as an exmaple to mimic data

- The raw data is then sent to Amazon Kinesis Firehose, where it can be stored securely on S3 bucket for future use and analytics.

- Amazon Kinesis Firehose is responsible for buffering and forwarding the data to Amazon OpenSearch service.
  - Helps optimize data delivery by batching and compressing the data as well as handling any errors that might occur

- Amazon Kinesis Data Analytics detects anomalies in the number of out-of-service beds.

- Again, the processed data is sent to Kinesis Data Streams, and then to Kinesis Data Firehose where it's filtered and buffered again and then forwarded to OpenSearch Services.

- The data is stored in OpenSearch service, which is a search and analytics engine that can be used to search, analyze, and visualize large amounts of data.

- Hospital staff can create dashboards in OpenSearch Service that provide insights into bed occupancy. The dashboard are accessible on desktops, laptops, and mobile device, and the staff can use the data to make

## Technologies Used
- Amazon Kinesis Data Analytics
- Amazon Kinesis Data Firehose
- Amazon OpenSearch service
- Amazon S3
