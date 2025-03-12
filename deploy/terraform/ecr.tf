# create registries
resource "aws_ecr_repository" "frontend" {
  name         = "arbor-lwa-frontend"
  force_delete = true
  image_scanning_configuration {
    scan_on_push = false
  }
}

resource "aws_ecr_repository" "backend" {
  name         = "arbor-lwa-backend"
  force_delete = true
  image_scanning_configuration {
    scan_on_push = false
  }
}

# build & push containers w/ docker.sh
resource "null_resource" "frontend_build" {
  triggers = {
    always_run = timestamp()
  }
  provisioner "local-exec" {
    command = "source ./docker.sh ${aws_ecr_repository.frontend.repository_url} '../../frontend' ${var.arbor_aws_region}"
  }
}

resource "null_resource" "backend_build" {
  triggers = {
    always_run = timestamp()
  }
  provisioner "local-exec" {
    command = "source ./docker.sh ${aws_ecr_repository.backend.repository_url} '../../backend' ${var.arbor_aws_region}"
  }
}