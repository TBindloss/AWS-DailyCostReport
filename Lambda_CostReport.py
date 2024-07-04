import boto3, datetime, os

# A  Python based Lambda function to send an SNS topic to notify users of the month to date costs.
# Requires an environmental variable named 'SNS_TOPIC_ARN' to be set with the ARN of the SNS topic to send the message to. Alternatively, replace line 27 with the ARN of the SNS topic.

def calculate_month_to_date_costs():
    ce_client = boto3.client('ce')
    today = datetime.date.today()
    start_date = datetime.date(today.year, today.month, 1)
    end_date = today
    response = ce_client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': end_date.strftime('%Y-%m-%d')
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
    )
    results = response['ResultsByTime']
    total_cost = float(results[0]['Total']['UnblendedCost']['Amount'])
    return total_cost
def lambda_handler(event, context):
    total_cost = calculate_month_to_date_costs()
    formatted_cost = "{:.2f}".format(total_cost)
    sns_client = boto3.client('sns')
    sns_client.publish(
        TopicArn=os.getenv('SNS_TOPIC_ARN'),
        Message=f"AWS costs for the month to date: ${formatted_cost}",
        Subject=f"AWS MTD cost: ${formatted_cost}"
    )