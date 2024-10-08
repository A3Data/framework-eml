variable "repository_name" {
  description = "Nome do repositório ECR"
  type        = string
  default     = "prediction-eml"
}

variable "region" {
  description = "A região onde a infraestrutura será criada."
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Nome do bucket S3 para o backend"
  type        = string
}
