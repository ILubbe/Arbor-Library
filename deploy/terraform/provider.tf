terraform {
  required_providers {
    null = {
      source = "hashicorp/null"
    }
  }
}

provider "aws" {
  region = var.arbor_aws_region
}