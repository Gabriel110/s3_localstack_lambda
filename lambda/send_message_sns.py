import json
import uuid
from http import HTTPStatus

import boto3
import os
import logging

from botocore.exceptions import ClientError

sns_url = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
sns = boto3.client('sns', aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1",
									 endpoint_url=sns_url)
topic_arn = 'arn:aws:sns:us-east-1:000000000000:lambda-process-bucket-topic'


def send_message(message):
	try:
		response = sns.publish(
			TopicArn=topic_arn,
			Message=message
		)

		return {
			'statusCode': 200,
			'body': json.dumps(response)
		}
	except Exception as e:
		print('Failed to publish message to SNS topic')
		return {'status': 'error', 'message': str(e)}


def mount_message_list(row_array, correlation_id):
	message_list = []
	for row in row_array:
		message = {
			'Id': str(uuid.uuid4()),
			'Message': json.dumps(row),
			'MessageAttributes': {
				'correlation_id': {
					'DataType': 'String',
					'StringValue': str(correlation_id)
				}
			}
		}
		message_list.append(message)
	return message_list


def _get_publish_response_code(response):
	response_metadata = response['ResponseMetadata']
	return response_metadata['HTTPStatusCode']


def send_message_batch_to_sns(row_array, correlation_id):
	message_list = mount_message_list(row_array, correlation_id)

	if not len(message_list):
		return {'result': HTTPStatus.OK.value}

	try:
		response = sns.publish_batch(
			TopicArn=topic_arn,
			PublishBatchRequestEntries=message_list
		)
		status_code = _get_publish_response_code(response)
		failed_messages_count = len(response["Failed"])
		if status_code == HTTPStatus.OK.value and failed_messages_count > 0:
			raise Exception(f'Falha ao publicar {failed_messages_count} mensagens de um total de {len(message_list)}')

	except ClientError as e:
		raise Exception('Falha ao publicar mensagem no tópico')
