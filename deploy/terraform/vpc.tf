resource "aws_vpc" "ecs_vpc" {
  cidr_block           = var.arbor_aws_vpc
  enable_dns_support   = true
  enable_dns_hostnames = true
}

resource "aws_subnet" "ecs_subnet" {
  vpc_id                  = aws_vpc.ecs_vpc.id
  cidr_block              = var.arbor_aws_ecs_subnet
  availability_zone       = var.arbor_aws_az_1
  map_public_ip_on_launch = true
}

resource "aws_subnet" "alb_subnet_1" {
  vpc_id                  = aws_vpc.ecs_vpc.id
  cidr_block              = var.arbor_aws_alb_subnet_1
  availability_zone       = var.arbor_aws_az_1
  map_public_ip_on_launch = true
}

resource "aws_subnet" "alb_subnet_2" {
  vpc_id                  = aws_vpc.ecs_vpc.id
  cidr_block              = var.arbor_aws_alb_subnet_2
  availability_zone       = var.arbor_aws_az_2
  map_public_ip_on_launch = true
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.ecs_vpc.id
}

resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.ecs_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "public_route_table_association_1" {
  subnet_id      = aws_subnet.alb_subnet_1.id
  route_table_id = aws_route_table.public_route_table.id
}

resource "aws_route_table_association" "public_route_table_association_2" {
  subnet_id      = aws_subnet.alb_subnet_2.id
  route_table_id = aws_route_table.public_route_table.id
}