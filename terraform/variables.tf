variable "aws_region" {
  type    = string
  default = "eu-west-3" # Paris
}

variable "environment" {
  type    = string
  default = "local" # 'local' pour LocalStack, 'prod' pour AWS
}

variable "bucket_name" {
  type    = string
  default = "edona-item-images-bucket"
}