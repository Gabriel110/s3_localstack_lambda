resource "random_pet" "bucket" {}

resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name
}


resource "aws_s3_object" "readme" {
  bucket       = aws_s3_bucket.bucket.id
  key          = "input/arquivos/${local.readme_file}"
  content_type = "text/markdown; charset=UTF-8"
  source       = local.readme_file_path
  etag         = filemd5(local.readme_file_path)
}


resource "aws_s3_bucket_notification" "s3_lambda_trigger" {
  bucket = aws_s3_bucket.bucket.id
  lambda_function {
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "input/arquivos"
    # filter_suffix       = ".txt"
    lambda_function_arn = aws_lambda_function.lambda_function.arn
  }
}

resource "aws_lambda_permission" "s3" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.bucket.arn
}