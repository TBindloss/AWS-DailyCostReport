# Terraform configuration
terraform {
  backend "s3" {
    bucket         = "tb-terraform-states-test"
    key            = "AWS-DailyCostReport/terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "Terraform_Locks"
    encrypt        = true
  }

  # Version constraints
  required_version = ">= 1.0.0"

  # Provider configurations
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

# AWS Provider configuration
provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
      ManagedBy = "Terraform"
      Project   = "AWS-DailyCostReport"
    }
  }
}