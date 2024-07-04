# AWS-DailyCostReport
Lambda function to email month to date AWS costs.

## Setup
- If one doesn't already exist - Create an SNS topic and add the various subscriptions. Take note of the ARN.
- A Lambda function using Python 3.12 runtime.
- Lambda functions role having the following permissions - SNS:Publish, ce:GetCostAndUsage
- A daily event bridge trigger for the Lambda function