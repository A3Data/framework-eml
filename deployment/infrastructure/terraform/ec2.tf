resource "tls_private_key" "private_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "aws_key_pair" "generated_key" {
  key_name   = "${local.default_prefix}-ec2-key"
  public_key = tls_private_key.private_key.public_key_openssh
}


data "aws_ami" "ecs_ami" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-ecs-hvm-*-x86_64-ebs"]
  }
}

resource "aws_instance" "ecs_instance" {
  ami           = data.aws_ami.ecs_ami.id
  instance_type = var.ec2_type
  key_name      = aws_key_pair.generated_key.key_name
  iam_instance_profile = aws_iam_instance_profile.ecs_instance_profile.name

  user_data = <<-EOF
    #!/bin/bash
    echo ECS_CLUSTER=${aws_ecs_cluster.eml_cluster.name} >> /etc/ecs/ecs.config
  EOF

  subnet_id = data.aws_subnets.default.ids[0]

  vpc_security_group_ids = [aws_security_group.app_sg.id]

  associate_public_ip_address = true

  tags = {
    Name = "${local.default_prefix}-ecs-instance"
  }
  depends_on = [aws_ecs_cluster.eml_cluster]
}