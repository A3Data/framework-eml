provider "aws" {
  region  = var.region
}
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.49"
    }
    tls = {
      source  = "hashicorp/tls"
      version = ">= 3.0"
    }
  }
  backend "s3" {
    key     = "terraform/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}


data "aws_caller_identity" "current" {}