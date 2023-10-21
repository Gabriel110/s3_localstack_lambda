resource "aws_sns_topic" "sns_topic" {
  name = var.lambda_process_bucket_topic
}

resource "aws_sns_topic_subscription" "queue_subscription" {
  protocol             = "sqs"
  raw_message_delivery = true
  topic_arn            = aws_sns_topic.sns_topic.arn
  endpoint             = aws_sqs_queue.queue.arn
}