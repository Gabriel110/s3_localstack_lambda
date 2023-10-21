data "aws_iam_policy_document" "s3_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["*"]
    }
  }
}

data "aws_iam_policy_document" "s3_policy_role" {
  statement {
    effect    = "Allow"
    actions   = ["s3:*"]
    resources = ["*"]
  }
}

resource "aws_iam_role" "s3_role" {
  name               = "s3-role"
  assume_role_policy = data.aws_iam_policy_document.s3_role_policy.json
}

resource "aws_iam_policy" "s3_policy" {
  name   = "s3-policy"
  policy = data.aws_iam_policy_document.s3_policy_role.json
}

resource "aws_iam_role_policy_attachment" "s3_full_acess" {
  role     = aws_iam_role.s3_role.name
  policy_arn = aws_iam_policy.s3_policy.arn
}


resource "aws_sqs_queue_policy" "queue_subscription" {
  queue_url = aws_sqs_queue.queue.id
  policy    = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "sns.amazonaws.com"
      },
      "Action": [
        "sqs:SendMessage"
      ],
      "Resource": [
        "${aws_sqs_queue.queue.arn}"
      ],
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${aws_sns_topic.sns_topic.arn}"
        }
      }
    }
  ]
}
EOF
}