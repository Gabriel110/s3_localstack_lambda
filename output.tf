# Output do projeto
output "lambda" {
  value = {
    arn        = aws_lambda_function.lambda_function.arn
    name       = aws_lambda_function.lambda_function.function_name
    invoke_arn = aws_lambda_function.lambda_function.invoke_arn
  }
}

output "bucket" {
  value = {
    arn  = aws_s3_bucket.bucket.arn
    name = aws_s3_bucket.bucket.id
    domain = aws_s3_bucket.bucket.bucket_regional_domain_name
  }
}