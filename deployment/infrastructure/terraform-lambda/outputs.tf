output "api_url" {
  value       = "https://${aws_api_gateway_rest_api.api.id}.execute-api.${var.region}.amazonaws.com/prod/predict"
  description = "URL do endpoint da API"
}
