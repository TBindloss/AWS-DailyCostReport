import boto3
import datetime
import os
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_month_date_range():
    """Get the start and end dates for the current month."""
    today = datetime.date.today()
    return datetime.date(today.year, today.month, 1), today

def calculate_month_to_date_costs(ce_client):
    """Calculate AWS costs from start of month to current date."""
    try:
        start_date, end_date = get_month_date_range()
        response = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost']
        )
        total_cost = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
        return total_cost
    except (ClientError, KeyError, ValueError) as e:
        logger.error(f"Error calculating costs: {str(e)}")
        raise

def lambda_handler(event, context):
    """AWS Lambda handler to publish month-to-date AWS costs via SNS."""
    try:
        # Initialize AWS clients
        ce_client = boto3.client('ce')
        sns_client = boto3.client('sns')
        
        # Get and validate SNS topic ARN
        topic_arn = os.getenv('SNS_TOPIC_ARN')
        if not topic_arn:
            raise ValueError("SNS_TOPIC_ARN environment variable not set")
        
        # Calculate and publish costs
        total_cost = calculate_month_to_date_costs(ce_client)
        formatted_cost = "{:.2f}".format(total_cost)
        
        sns_client.publish(
            TopicArn=topic_arn,
            Message=f"AWS costs for month to date: ${formatted_cost}",
            Subject=f"AWS MTD cost: ${formatted_cost}"
        )
        
        logger.info(f"Published cost notification: ${formatted_cost}")
        return {
            'statusCode': 200,
            'body': 'Cost notification sent successfully'
        }
    
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        raise  # Let Lambda handle the error and retry logic
