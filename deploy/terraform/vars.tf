variable "my_domain_name" {
  type    = string
  default = "arbor-library.click"
}

variable "arbor_aws_region" {
  type    = string
  default = "us-west-2"
}

variable "arbor_aws_az_1" {
  type    = string
  default = "us-west-2a"
}

variable "arbor_aws_az_2" {
  type    = string
  default = "us-west-2b"
}

variable "arbor_aws_vpc" {
  type    = string
  default = "10.0.0.0/16"
}

variable "arbor_aws_ecs_subnet" {
  type    = string
  default = "10.0.0.0/24"
}

variable "arbor_aws_alb_subnet_1" {
  type    = string
  default = "10.0.1.0/24"
}

variable "arbor_aws_alb_subnet_2" {
  type    = string
  default = "10.0.2.0/24"
}