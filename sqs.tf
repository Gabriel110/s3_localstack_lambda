resource "aws_sqs_queue" "queue" {
  name                      = var.lambda_process_bucket_queue
  receive_wait_time_seconds = 20
  message_retention_seconds = 18400
}
