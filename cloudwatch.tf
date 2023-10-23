# resource "aws_cloudwatch_log_group" "log-group" {
#   name              = "/aws/lambda/${aws_lambda_function.lambda_function.function_name}"
#   retention_in_days = 30
# }