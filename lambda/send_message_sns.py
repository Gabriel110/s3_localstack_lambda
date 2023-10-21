import json
import boto3
import os

sns_url = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
sns = boto3.client('sns', aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1", endpoint_url=sns_url)
topic_arn = 'arn:aws:sns:us-east-1:000000000000:lambda-process-bucket_queue'


def send_message(message):
    try:
      response = sns.publish(
        TopicArn=topic_arn,
        Message= message
      )

      return {
        'statusCode': 200,
        'body': json.dumps(response)
      }
    except Exception as e:
      print('Failed to publish message to SNS topic')
      return {'status': 'error', 'message': str(e)}