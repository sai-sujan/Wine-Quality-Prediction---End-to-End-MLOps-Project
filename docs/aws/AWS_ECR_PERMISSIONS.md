# AWS Permissions Required for Docker Lambda Deployment

## GitHub Actions User Permissions

The AWS user whose credentials are stored in GitHub Secrets needs the following permissions:

### 1. ECR (Elastic Container Registry) Permissions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:CreateRepository",
        "ecr:DescribeRepositories",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "*"
    }
  ]
}
```

### 2. Lambda Permissions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:CreateFunction",
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration",
        "lambda:GetFunction",
        "lambda:AddPermission",
        "lambda:WaitFunctionUpdated"
      ],
      "Resource": "arn:aws:lambda:us-east-2:*:function:wine-quality-predictor"
    }
  ]
}
```

### 3. IAM Permissions (for role creation)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iam:CreateRole",
        "iam:GetRole",
        "iam:AttachRolePolicy",
        "iam:PutRolePolicy",
        "iam:PassRole"
      ],
      "Resource": "arn:aws:iam::*:role/wine-quality-lambda-role"
    }
  ]
}
```

### 4. API Gateway Permissions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "apigateway:GET",
        "apigateway:POST",
        "apigateway:PUT",
        "apigateway:PATCH"
      ],
      "Resource": "arn:aws:apigateway:us-east-2::*"
    }
  ]
}
```

### 5. S3 Permissions (existing)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::wine-quality-mlops-sujan",
        "arn:aws:s3:::wine-quality-mlops-sujan/*"
      ]
    }
  ]
}
```

## Quick Setup

If you're creating a new IAM user for GitHub Actions:

1. Go to AWS IAM Console
2. Create a new user or select existing user
3. Attach these managed policies:
   - `AmazonEC2ContainerRegistryFullAccess` (for ECR)
   - `AWSLambda_FullAccess` (for Lambda)
   - `IAMFullAccess` (for role creation) - OR create custom policy above
   - `AmazonAPIGatewayAdministrator` (for API Gateway)
   - Custom S3 policy (see above)

4. Generate access keys
5. Add to GitHub Secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

## Minimal Permission Set (Recommended)

Instead of using FullAccess policies, combine the custom policies above for least privilege access.
