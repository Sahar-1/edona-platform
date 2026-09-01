terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = var.aws_region
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true # <-- Empeche le blocage d'URL sous-domaine

  endpoints {
    s3 = "http://localhost:4566"
  }
}
resource "aws_s3_bucket" "edona_storage" {
  bucket        = var.bucket_name
  force_destroy = true

  tags = {
    Name        = "EDONA Storage Bucket"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_public_access_block" "edona_storage_acl" {
  bucket = aws_s3_bucket.edona_storage.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}