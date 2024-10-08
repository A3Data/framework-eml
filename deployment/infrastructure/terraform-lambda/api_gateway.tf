resource "aws_api_gateway_rest_api" "api" {
  name        = "PredictionAPI"
  description = "API para a função Lambda de previsão"
}

resource "aws_api_gateway_resource" "predict" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "predict"
}

resource "aws_api_gateway_method" "predict_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.predict.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "predict_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.predict.id
  http_method             = aws_api_gateway_method.predict_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.prediction_eml_lambda.arn}/invocations"
}

resource "aws_api_gateway_deployment" "api_deployment" {
  depends_on = [aws_api_gateway_integration.predict_integration]
  rest_api_id = aws_api_gateway_rest_api.api.id
  stage_name  = "prod"
}