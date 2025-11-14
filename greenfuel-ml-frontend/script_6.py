
# Create AWS deployment guide and Python script to push to GitHub
import json

# Create detailed AWS deployment guide
aws_deployment_guide = '''# AWS Deployment Guide for GreenFuel-ML

## Step-by-Step AWS Deployment

### Prerequisites
1. AWS Account with free tier eligibility
2. AWS CLI installed: `pip install awscli`
3. AWS SAM CLI: `pip install aws-sam-cli`
4. Git installed and configured

### Step 1: Configure AWS Credentials

```bash
aws configure
```

Enter your AWS credentials when prompted:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: us-east-1
- Output format: json

### Step 2: Build the Application

```bash
sam build
```

### Step 3: Deploy to AWS (First Time)

```bash
sam deploy --guided
```

Follow the prompts:
- Stack Name: `greenfuel-ml-prod`
- Region: `us-east-1`
- Confirm changes before deploy: `y`
- Allow SAM CLI to create roles: `y`

### Step 4: Get Your API Endpoint

After deployment completes, you'll see output like:

```
CloudFormation outputs from deployed stack
-----------------------------------------
Outputs
Key                 Value
---                 -----
ApiEndpoint         https://XXXXXXXXXX.execute-api.us-east-1.amazonaws.com/prod/
```

**Save this URL** - you'll need it for the frontend.

### Step 5: Update Frontend

In `index.html`, find this line:

```javascript
const API_BASE_URL = 'http://localhost:5000';
const USE_MOCK_PREDICTIONS = true;
```

Replace with:

```javascript
const API_BASE_URL = 'https://XXXXXXXXXX.execute-api.us-east-1.amazonaws.com/prod';
const USE_MOCK_PREDICTIONS = false;
```

### Step 6: Redeploy Frontend

```bash
git add index.html
git commit -m "Update API endpoint for AWS"
git push origin main
```

## Cost Estimation (AWS Free Tier)

| Service | Free Tier Limit | Expected Usage |
|---------|-----------------|-----------------|
| Lambda | 1M requests/month | ~100K requests |
| API Gateway | 1M requests/month | Included |
| CloudWatch Logs | 5GB ingestion | Minimal |
| DynamoDB | 25GB storage | Minimal |
| Data Transfer | 1GB/month | Minimal |

**Expected Cost: $0 USD/month** (within free tier)

## Monitoring and Logs

### View Lambda Logs
```bash
aws logs tail /aws/lambda/greenfuel-predict-prod --follow
```

### Monitor API Usage
```bash
# View API metrics
aws cloudwatch get-metric-statistics \\
  --namespace AWS/ApiGateway \\
  --metric-name Count \\
  --dimensions Name=ApiName,Value=greenfuel-api-prod \\
  --start-time 2025-01-01T00:00:00Z \\
  --end-time 2025-01-02T00:00:00Z \\
  --period 3600 \\
  --statistics Sum
```

## Troubleshooting

### Issue: CORS Errors
**Solution:** CORS is configured in the API Gateway. Ensure you're using the correct endpoint URL.

### Issue: Model Not Found
**Solution:** Ensure `.pkl` files are in the root directory before deployment.

### Issue: Timeout Errors
**Solution:** Increase Lambda timeout or memory in template.yaml:

```yaml
Timeout: 120
MemorySize: 1024
```

## Updating Deployment

After making changes:

```bash
sam build
sam deploy
```

## Cleanup (Delete Resources)

To avoid unexpected charges, delete the stack:

```bash
aws cloudformation delete-stack --stack-name greenfuel-ml-prod
```

## Additional AWS Services

### Enable CloudWatch Alarms
```bash
# Create alarm for high error rate
aws cloudwatch put-metric-alarm \\
  --alarm-name greenfuel-errors \\
  --alarm-description "Alert on Lambda errors" \\
  --metric-name Errors \\
  --namespace AWS/Lambda \\
  --statistic Sum \\
  --period 300 \\
  --threshold 10 \\
  --comparison-operator GreaterThanThreshold
```

### Set Up Auto-Scaling
DynamoDB auto-scales automatically with on-demand billing.

## Next Steps

1. Deploy to production
2. Set up CloudWatch monitoring
3. Configure CloudFront for faster delivery
4. Add authentication with API keys
5. Set up CI/CD pipeline with GitHub Actions

## Support

For AWS-specific issues, visit:
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
'''

with open('greenfuel-ml-frontend/AWS_DEPLOYMENT.md', 'w') as f:
    f.write(aws_deployment_guide)

print("✓ Created AWS_DEPLOYMENT.md")
