import boto3

s3 = boto3.client('s3',
                  endpoint_url='https://localhost:9000',
                  aws_access_key_id='BsvW9jlpYX8TvD9F',
                  aws_secret_access_key='HrGdJapKsXbKEcXABWNQ2CO15v3y9MMk',
                  verify=False,
                  region_name='us-east-1')

r = s3.select_object_content(
    Bucket='uniovi',
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