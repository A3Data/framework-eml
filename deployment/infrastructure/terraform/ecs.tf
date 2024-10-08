resource "aws_cloudwatch_log_group" "ecs_service_logs" {
  name              = "/ecs/${local.default_prefix}"
  retention_in_days = 7
}

data "aws_ecr_repository" "back" {
  name = "${var.repo_name}"
}

resource "aws_ecs_task_definition" "service" {
  family                   = "${local.default_prefix}-service"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu = 512
  memory = 1024
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  container_definitions    = jsonencode(
    [
      {
        "name": "backend",
        "image": "${data.aws_ecr_repository.back.repository_url}:latest",
        "cpu": 256,
        "memory": 512,
        "essential": true,
        "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
            "awslogs-group": "${aws_cloudwatch_log_group.ecs_service_logs.name}",
            "awslogs-region": "${var.aws_region}",
            "awslogs-stream-prefix": "backend"
          }
        }
      }
    ]
  )

  tags = {
    Name = local.default_prefix
  }
}

resource "aws_ecs_cluster" "eml_cluster" {
  name = "${local.default_prefix}-cluster"
  tags = {
    Name = local.default_prefix
  }
}