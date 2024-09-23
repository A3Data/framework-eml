resource "aws_cloudwatch_log_group" "ecs_service_logs" {
  name              = "/ecs/${local.default_prefix}"
  retention_in_days = 7
}

data "aws_ecr_repository" "back" {
  name = "${local.default_prefix}-api"
}

resource "aws_ecs_task_definition" "service" {
  family                   = "${local.default_prefix}-service"
  network_mode             = "host"
  requires_compatibilities = ["EC2"]
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
        "portMappings": [
          {
            "containerPort": "${var.api_port}"
          }
        ],
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

resource "aws_ecs_service" "eml" {
  name            = "${local.default_prefix}-service"
  cluster         = aws_ecs_cluster.eml_cluster.id
  task_definition = aws_ecs_task_definition.service.arn
  desired_count   = 1
  launch_type     = "EC2"
  enable_ecs_managed_tags = true
  wait_for_steady_state = true

  tags = {
    Name = local.default_prefix
  }

  depends_on = [
    aws_instance.ecs_instance
  ]
}
