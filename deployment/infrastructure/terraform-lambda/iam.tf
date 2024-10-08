data "aws_iam_role" "existing_role" {
  name = "prediction_eml_role"
}

resource "aws_iam_role" "prediction_eml_role" {
  count              = length(data.aws_iam_role.existing_role.*.name) == 0 ? 1 : 0
  name               = "prediction_eml_role"

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

resource "aws_iam_policy_attachment" "prediction_eml_policy_attachment" {
  count      = length(data.aws_iam_role.existing_role.*.name) == 0 ? 1 : 0
  name       = "prediction_eml_policy_attachment"
  roles      = [aws_iam_role.prediction_eml_role[0].name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
