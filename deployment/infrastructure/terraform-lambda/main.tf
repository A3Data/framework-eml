terraform {
  backend "s3" {
    bucket  = var.bucket_name
    key     = "terraform/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

resource "aws_lambda_function" "prediction_eml_lambda" {
  function_name = "prediction_eml"
  role          = aws_iam_role.prediction_eml_role.arn
  package_type  = "Image"
  image_uri     = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com/${var.repository_name}:latest"

  memory_size = 256
  timeout     = 120
}

resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.prediction_eml_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}
