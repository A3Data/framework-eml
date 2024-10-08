resource "aws_iam_role" "prediction_test_role" {
  name               = "prediction_test_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Effect    = "Allow"
        Sid       = ""
      },
    ]
  })
}

resource "aws_iam_policy_attachment" "prediction_test_policy_attachment" {
  name       = "prediction_test_policy_attachment"
  roles      = [aws_iam_role.prediction_test_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
