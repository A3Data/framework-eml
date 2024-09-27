variable "api_port" {
  description = "Port for the FastAPI application"
  default     = 8000
}

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "Região para provisionar os recursos na AWS"
}

variable "project_name" {
  description = "Nome do projeto: eml"
  type        = string
  default     = "eml"
}

variable "ec2_type" {
  description = "Tipo da instancia de ec2 para ser lançada junto do ecs"
  type = string
  default = "t2.small"
}

locals {
  tags = {
    project     = var.project_name
    partner     = "a3data"
    created-by  = "terraform"
  }
  default_prefix = "${var.project_name}"
}