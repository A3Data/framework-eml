# Recurso para agendar a task
resource "aws_cloudwatch_event_rule" "ecs_task_schedule" {
  name                = "${local.default_prefix}-ecs-schedule"
  schedule_expression = "${var.batch_interval}"  # Executa a cada 5 minutos

  tags = {
    Name = local.default_prefix
  }
}

resource "aws_cloudwatch_event_target" "ecs_task_target" {
  rule      = aws_cloudwatch_event_rule.ecs_task_schedule.name
  arn       = aws_ecs_cluster.eml_cluster.arn
  role_arn  = aws_iam_role.eventbridge_ecs_role.arn

  ecs_target {
    task_definition_arn = aws_ecs_task_definition.service.arn
    launch_type         = "FARGATE"
    network_configuration {
      subnets          = data.aws_subnets.default.ids
      security_groups  = [aws_security_group.app_sg.id]
      assign_public_ip = true
    }
  }
}


resource "aws_iam_role" "eventbridge_ecs_role" {
  name = "${local.default_prefix}-eventbridge-ecs-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = [
            "events.amazonaws.com",
            "scheduler.amazonaws.com"
          ]
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Permissão para o EventBridge invocar a task do ECS
resource "aws_iam_role_policy" "allow_eventbridge_invoke_ecs" {
  role = aws_iam_role.eventbridge_ecs_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = "ecs:RunTask",
        Resource = aws_ecs_task_definition.service.arn
      },
      {
        Effect = "Allow",
        Action = "iam:PassRole",
        Resource = "*"
      }
    ]
  })
}