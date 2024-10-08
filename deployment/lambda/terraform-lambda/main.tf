resource "aws_ecr_repository" "prediction_test_repository" {
  name = "prediction-test-repo"
}

resource "aws_lambda_function" "prediction_test_lambda" {
  function_name = "prediction_test"
  role          = aws_iam_role.prediction_test_role.arn
  package_type  = "Image"  # Indica que a função Lambda usa uma imagem Docker
  image_uri     = "${aws_ecr_repository.prediction_test_repository.repository_url}:latest"

  memory_size = 256
  timeout     = 120
}

resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.prediction_test_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}
