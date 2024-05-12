# Description
Documentation Deploy Minio Docker

## Steps

Create a deployment file for docker compose like this with the environment variable **MINIO_API_SELECT_PARQUET** set to **on** to manage parquet files in minio server

```shell
version: '3.8'

services:
  minio:
    container_name: minio_local
    image: minio/minio:latest
    ports:
      - '9010:9000'
      - '9100:9090'
    environment:
      - MINIO_ROOT_USER=${MINIO_ROOT_USER}
      - MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD}
      - MINIO_CONFIG_ENV_FILE=/etc/config.env
      - MINIO_API_SELECT_PARQUET=on
    volumes:
      - ./data:/mnt/data
      - ./credentials/.env.dev:/etc/config.env
    command: server --console-address ":9090"
    networks:
      - minio-net

networks:
  minio-net:
    external: true
```

Execute the deployment:

```shell
docker-compose -d up
```

We can access to Minio operator at this url and create a bucket called **samples** and upload the file **people.parquet** to test from python

```shell
http://localhost:9100

```

Execute this python sample to load the parquet file **people.parquet**

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
