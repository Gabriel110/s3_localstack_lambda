variable "lamba_name" {
  type        = string
  description = ""
  default     = "lambda-process-bucket"
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "bucket_name" {
  type        = string
  description = ""
  default     = "file-bucket-122345"
}

variable "lambda_process_bucket_topic" {
  type        = string
  description = ""
  default     = "lambda-process-bucket-topic"
}

variable "lambda_process_bucket_queue" {
  type        = string
  description = ""
  default     = "lambda-process-bucket"
}

variable "service_domain" {
  type        = string
  description = ""
  default     = "api"
}