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

variable "batch_interval" {
  description = "Cron que irá ditar o intervalo que o batch deve rodar"
  type        = string
  default     = "cron(0 23 */1 * ? *)"
}


locals {
  tags = {
    project     = var.project_name
    partner     = "a3data"
    created-by  = "terraform"
  }
  default_prefix = "${var.project_name}"
}