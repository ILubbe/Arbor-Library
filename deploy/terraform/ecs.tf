resource "aws_iam_role" "ecs_execution_role" {
  name = "ecs-execution-role"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "",
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "ecs-tasks.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "ecs_execution_role_policy" {
  name = "ecs-execution-role-policy"
  role = aws_iam_role.ecs_execution_role.name

  # additional permissions for ECR
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer"
        ]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = "logs:*"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution_role_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_task_definition" "arbor_lwa_task" {
  family                   = "arbor-lwa-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "2048"
  memory                   = "4096"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "mariadb"
      image     = "docker.io/library/mariadb:11.6.2"
      essential = true
      environment = [
        { name = "MARIADB_ROOT_PASSWORD", value = "arbor" },
        { name = "MARIADB_DATABASE", value = "arbor" },
        { name = "MARIADB_USER", value = "arbor" },
        { name = "MARIADB_PASSWORD", value = "arbor" }
      ]
      portMappings = [
        { containerPort = 3306, hostPort = 3306 }
      ]
      "logConfiguration" : {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-create-group" : "true",
          "awslogs-group" : "arbor-lwa-logs",
          "awslogs-region" : var.arbor_aws_region,
          "awslogs-stream-prefix" : "mariadb"
        }
      },
    },
    {
      name      = "elasticsearch"
      image     = "docker.io/library/elasticsearch:8.17.1"
      essential = true
      environment = [
        { name = "discovery.type", value = "single-node" },
        { name = "xpack.security.enabled", value = "false" }
      ]
      portMappings = [
        { containerPort = 9200, hostPort = 9200 }
      ]
      "logConfiguration" : {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-create-group" : "true",
          "awslogs-group" : "arbor-lwa-logs",
          "awslogs-region" : var.arbor_aws_region,
          "awslogs-stream-prefix" : "elasticsearch"
        }
      },
    },
    {
      name      = "redis"
      image     = "docker.io/library/redis:7.4.2"
      essential = true
      portMappings = [
        { containerPort = 6379, hostPort = 6379 }
      ]
      "logConfiguration" : {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-create-group" : "true",
          "awslogs-group" : "arbor-lwa-logs",
          "awslogs-region" : var.arbor_aws_region,
          "awslogs-stream-prefix" : "redis"
        }
      },
    },
    {
      name      = "backend"
      image     = "${aws_ecr_repository.backend.repository_url}"
      essential = true
      environment = [
        { name = "DB_USER", value = "arbor" },
        { name = "DB_PASSWORD", value = "arbor" },
        { name = "DB_HOST", value = "localhost" },
        { name = "DB_PORT", value = "3306" },
        { name = "DB_NAME", value = "arbor" },
        { name = "REDIS_HOST", value = "localhost" },
        { name = "REDIS_PORT", value = "6379" },
        { name = "ELASTICSEARCH_HOST", value = "localhost" },
        { name = "ELASTICSEARCH_PORT", value = "9200" },
        { name = "JWT_SECRET_KEY", value = "arbor1234567890arbor1234567890arbor1234567890" },
        { name = "SEED_BOOK_COUNT", value = "221" }
      ]
      portMappings = [
        { containerPort = 5000, hostPort = 5000 }
      ]
      "logConfiguration" : {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-create-group" : "true",
          "awslogs-group" : "arbor-lwa-logs",
          "awslogs-region" : var.arbor_aws_region,
          "awslogs-stream-prefix" : "backend"
        }
      },
      command = ["/bin/sh", "-c", "sleep 30 && python app.py"]
    },
    {
      name      = "frontend"
      image     = "${aws_ecr_repository.frontend.repository_url}"
      essential = true
      portMappings = [
        { containerPort = 80, hostPort = 80 }
      ]
      "logConfiguration" : {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-create-group" : "true",
          "awslogs-group" : "arbor-lwa-logs",
          "awslogs-region" : var.arbor_aws_region,
          "awslogs-stream-prefix" : "frontend"
        }
      },
      command = ["/bin/sh", "-c", "nginx -g 'daemon off;'"]
    }
  ])
}

# attach to alb
resource "aws_ecs_service" "arbor_lwa_service" {
  name            = "arbor-lwa-service"
  cluster         = aws_ecs_cluster.arbor_lwa_cluster.id
  task_definition = aws_ecs_task_definition.arbor_lwa_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = [aws_subnet.alb_subnet_1.id, aws_subnet.alb_subnet_2.id]
    security_groups  = [aws_security_group.alb_sg.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.frontend_target_group.arn
    container_name   = "frontend"
    container_port   = 80
  }
  depends_on = [aws_lb_listener.https_listener]
}

resource "aws_ecs_cluster" "arbor_lwa_cluster" {
  name = "arbor-lwa-cluster"
}