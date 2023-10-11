import logging
import boto3
import os


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)



def read_message_s3(local_path):
  global row
  with open(local_path, 'r') as file:
    row = file.read()
  return row


def handler(event, context):
  endpoint_url =  'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
  s3 = boto3.client('s3', endpoint_url=endpoint_url, region_name='us-east-1', verify=False) 
  for record in event['Records']:
    bucket_name = record['s3']['bucket']['name']
    object_key = record['s3']['object']['key']

    local_path = os.path.join('/tmp', os.path.basename(object_key))
    s3.download_file(bucket_name, object_key, local_path)

    text = read_message_s3(local_path)
    print(text)
    
  return event