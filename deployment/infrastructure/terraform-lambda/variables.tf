variable "repository_name" {
  description = "Nome do repositório ECR"
  type        = string
  default     = "prediction-eml"
}

variable "region" {
  description = "A região onde a infraestrutura será criada."
  default     = "us-east-1"
}
