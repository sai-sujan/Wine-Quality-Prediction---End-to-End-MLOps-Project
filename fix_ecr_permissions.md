# Fix ECR Permissions for Lambda - Manual Steps

## The Real Problem

Lambda service needs permission to PULL the Docker image from ECR when creating the function.
This is DIFFERENT from the Lambda execution role permissions.

## Solution: Add ECR Repository Policy (Manual)

Since your user doesn't have `ecr:SetRepositoryPolicy` permission, you need to either:

### Option 1: Ask AWS Admin to Add Permission

Ask your AWS admin to add this permission to your IAM user:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ecr:SetRepositoryPolicy",
      "Resource": "*"
    }
  ]
}
```

### Option 2: Admin Sets ECR Policy Manually

Ask your AWS admin to set this policy on the ECR repository `wine-quality-lambda`:

1. Go to AWS Console → ECR → Repositories → wine-quality-lambda
2. Select the repository
3. Click "Permissions" tab
4. Click "Edit policy JSON"
5. Add this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "LambdaECRImageRetrievalPolicy",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": [
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer",
        "ecr:GetAuthorizationToken"
      ]
    }
  ]
}
```

### Option 3: Use AWS CLI with Admin Credentials

If you have access to admin AWS credentials temporarily:

```bash
aws ecr set-repository-policy \
    --repository-name wine-quality-lambda \
    --policy-text '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "LambdaECRImageRetrievalPolicy",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": [
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer"
      ]
    }
  ]
}' \
    --region us-east-2
```

## Why This Is Needed

1. **Lambda Function Creation**: When you create a Lambda from ECR image, Lambda SERVICE pulls the image
2. **ECR Repository Policy**: Controls WHO can pull images from ECR
3. **Lambda Execution Role**: Controls what the function can do AFTER it starts running

These are THREE DIFFERENT permission layers!

## After Fixing Permissions

Once the ECR repository policy is set, run:

```bash
./deploy_lambda_docker.sh
```

It should work!
