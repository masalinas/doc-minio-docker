# Description
Documentation Deploy Minio Docker

## Steps

```shell
docker-compose -d up
```

We can accedd to Minio operator at this url and create a buket called samples and upload the file people.parquet to test from python

```shell
http://localhost:9100

```

We can execute this sample to test

```shell
import boto3

s3 = boto3.client('s3',
                  endpoint_url='http://localhost:9010',
                  aws_access_key_id='admin',
                  aws_secret_access_key='password',
                  region_name='us-east-1')

r = s3.select_object_content(
    Bucket='samples',
    Key='people.parquet',
    ExpressionType='SQL',
    Expression="select * from s3object",
    InputSerialization={'Parquet': {}},
    OutputSerialization={'CSV': {}},
)

for event in r['Payload']:
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        print(records)
    elif 'Stats' in event:
        statsDetails = event['Stats']['Details']
        print("Stats details bytesScanned: ")
        print(statsDetails['BytesScanned'])
        print("Stats details bytesProcessed: ")
        print(statsDetails['BytesProcessed'])
```