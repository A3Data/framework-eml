output "private_key_pem" {
  description = "A chave privada SSH para acessar a instância EC2"
  value       = tls_private_key.private_key.private_key_pem
  sensitive   = true
}

output "ec2_public_ip" {
  description = "O IP público da instância EC2"
  value       = "${aws_instance.ecs_instance.public_ip}:${var.api_port}"
}
