resource "aws_lambda_function" "lambda_function" {
  function_name    = var.lamba_name
  filename         = data.archive_file.lambda_zip_file.output_path
  source_code_hash = data.archive_file.lambda_zip_file.output_base64sha256
  handler          = "handler.handler"
  role             = aws_iam_role.s3_role.arn
  runtime          = "python3.8"
  memory_size      = 512
  timeout          = 60

  lifecycle {
    create_before_destroy = true
  }

  environment {
    variables = {
      CHUNK_SIZE = "1024"
      MINIMUM_REMAINING_TIME_MS = "10000"
    }
  }
}

data "archive_file" "lambda_zip_file" {
  output_path = "${path.module}/lambda_zip/lambda.zip"
  source_dir  = "${path.module}/lambda"
  excludes    = ["__init__.py", "*.pyc"]
  type        = "zip"
}

# resource "aws_lambda_event_source_mapping" "event_source_mapping" {
#   event_source_arn  = aws_sqs_queue.queue.arn
#   function_name     = aws_lambda_function.lambda_function.arn
#   enabled           = true
#   batch_size        = 1
#   starting_position = "LATEST"
# }