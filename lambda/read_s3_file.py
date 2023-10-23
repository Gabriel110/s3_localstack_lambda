import csv
import os

import boto3
import botocore


class ReadFileS3:
  endpoint_url = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
  bucket_name: str
  object_key: str
  correlation_id: str
  offset: int
  s3_resource = boto3.resource('s3', endpoint_url=endpoint_url, region_name='us-east-1', verify=False)
  s3_object = None
  body_lines = None

  def __init__(self, bucket_name, object_key, correlation_id, offset):
    self.offset = offset
    self.correlation_id = correlation_id
    self.object_key = object_key
    self.bucket_name = bucket_name
    self.s3_object = self.s3_resource.Object(bucket_name=self.bucket_name, key=self.object_key)
    self.body_lines = self.get_object_body_lines(self.s3_object)

  def get_csv_reader(self):
    chunk_size = int(os.getenv("CHUNK_SIZE")) or 1024
    csv.register_dialect('lambda', 'excel', delimiter=';')
    return csv.DictReader(self.body_lines.iter_lines(chunk_size), fieldnames=self.get_field_names(), dialect='lambda')

  def get_object_body_lines(self, s3_object):
    try:
      resp = s3_object.get(Range=f'bytes={self.offset}-')
      body: botocore.response.StreamingBody = resp['Body']
      return BodyLines(body)
    except Exception as e:
      raise e

  def move_file_to_processed_folder(self):
    try:
      s3 = boto3.client('s3', endpoint_url=self.endpoint_url, region_name='us-east-1', verify=False)
      old_key = str(self.object_key)
      new_key = 'processados/' + old_key
      copy_source = {
        'Bucket': self.bucket_name,
        'Key': self.object_key
      }
      s3.copy_object(CopySource=copy_source, Bucket=self.bucket_name, Key=new_key)
      s3.delete_object(Bucket=self.bucket_name, Key=self.object_key)
      return
    except Exception as e:
      raise e

  def get_field_names(self):
    return ['id','set_name','set_code','num_of_cards','tcg_date']


class BodyLines:
  def __init__(self, body: botocore.response.StreamingBody, initial_offset=0):
    self.body = body
    self.offset = initial_offset

  def iter_lines(self, chunk_size):
    pending = b''
    for chunk in self.body.iter_chunks(chunk_size):
      lines = (pending + chunk).splitlines(True)
      for line in lines[:-1]:
        self.offset += len(line)
        yield line.decode('utf-8')
      pending = lines[-1]
    if pending:
      self.offset += len(pending)
      yield pending.decode('utf-8')
