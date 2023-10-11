variable "lamba_name" {
  type        = string
  description = ""
  default     = "lambda-process-gabriel"
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "bucket_name" {
  type        = string
  description = ""
  default     = "gabriel-bucket-122345"
}


variable "service_domain" {
  type        = string
  description = ""
  default     = "api"
}