# Hybrid Solution For PACS

## Objectives
The hospital's Medical Imaging department has a very large on-premises storage structure, storing images PACS.
They would like to use the power of cloud computing to reduce costs and streamline the process of archiving old images.

### Targeted KPI
- Increase overall patient satisfaction
- Improve average patient wait times
- Improve medical equipment utilization

## HLD
This solution creates a hybrid storage system between on-premises environments and AWS with the use case for a PACS.

## LLD
- For this solution, a PACS server maintains access to diagnostic tool spanning several years. New and frequently accesses data is stored on premises.
- The on-premises PACS server uses AWS storage Gateway which provides on-premises access to virtually unlimited cloud storage.
  - With S3 file gateway, configured s3 buckets are available as Network File Systems (NFS) mounts or Server Message Block (SMB) file shares.
- With S3 storage gateway, users can store and retrieve objects in S3 bucket by using file protocols such as NFS and SMB. Objects written through s3 File Gateway can be directly accessed in S3.
- On premises, users can deploy a VM the contains the Storage Gateway software on VMware ESXi, Microsoft Hyper-V, or Linux KVM. Users can also deploy Storage Gateway as a hardware appliance.
  - Alternatively, users can also deploy the Storage Gateway VM in VMware cloud on AWS, or as an Amazon Machine (AMI) in EC2.
- The most recently used data is cached on the gateway for low-latency access. Data transfer between the on-premises data center and AWS is fully managed and optimized by the gateway.
- Storage Gateway uses SSL/TLS to encrypt data that is transferred between a gateway appliance and AWS storage.
- Dicoogle, an open source PACS solution will be used for demonstration purposes.
- S3 bucket configured with S3 intelligent tiering, stores the DICOM files used in a PACS.
  - Designed to optimize storage costs by automatically moving data to the most cost-effective access tier when access pattern changes.
- As DICOM files age and are accessed less frequently, s3 intelligent-tiering moves the respective object to s3 standard Infrequent Access.
  - To get the lowest storage cost on data that needs to be accessed in minutes to hours users can activate archiving capabilities. They can move objects to the Archive or Deep Archive access tiers.


## Technologies Used
- Amazon Storage Gateways
- Amazon S3 Storage Gateway
- Amazon S3
- Dicoogle opensource PACS solution
