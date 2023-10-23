import json
import logging
import uuid
import	os
import boto3

from read_s3_file import ReadFileS3
from send_message_sns import send_message_batch_to_sns

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

MINIMUN_REMAINING_TIME_MS = int(os.getenv('MINIMUM_REMAINING_TIME_MS')) or 10000

endpoint_url = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']

def invoke_lambda(function_name, event):
	payload = json.dumps(event).encode('utf-8')
	client = boto3.client('lambda', endpoint_url=endpoint_url, region_name='us-east-1', verify=False)
	client.invoke(
		FunctionName=function_name,
		InvocationType='Event',
		Payload=payload
	)


def offset_invoke_send_message_batch_to_sns(bucket_name, object_key, correlation_id, offset, event, context):
	file = ReadFileS3(bucket_name, object_key, correlation_id, offset)

	row_batch_array = []
	for row in file.get_csv_reader():
		row_batch_array.append(row)
		if len(row_batch_array) >= 10:
			send_message_batch_to_sns(row_batch_array, correlation_id)
			row_batch_array.clear()
		if context.get_remaining_time_in_millis() < MINIMUN_REMAINING_TIME_MS: break

	send_message_batch_to_sns(row_batch_array, correlation_id)

	new_offset = offset + file.body_lines.offset
	if new_offset < file.s3_object.content_length:
		new_event = {
			**event,
			"offset": new_offset,
			"correlation_id": correlation_id
		}
		invoke_lambda(context.function_name, new_event)
	else:
		# file.move_file_to_processed_folder()
		return

def handler(event, context):
	record = event['Records'][0]
	bucket_name = record['s3']['bucket']['name']
	object_key = record['s3']['object']['key']
	correlation_id = event.get('correlation_id', str(uuid.uuid4()))
	offset = event.get('offset', 0)
    
	offset_invoke_send_message_batch_to_sns(bucket_name, object_key, correlation_id, offset, event, context)
	