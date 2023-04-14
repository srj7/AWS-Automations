import boto3
import os
from dotenv import load_dotenv

load_dotenv()

source_region = os.getenv('SOURCE_REGION')
target_region = os.getenv('TARGET_REGION')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

cloudwatch_source = boto3.client('cloudwatch', region_name=source_region,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)

try:
    # Describe all alarms in the source region
    response = cloudwatch_source.describe_alarms()
except Exception as e:
    print(f"Error occurred while describing alarms in the source region: {e}")
    exit(1)

cloudwatch_target = boto3.client('cloudwatch', region_name=target_region,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)

if 'MetricAlarms' not in response:
    print("No alarms found in the source region.")
    exit(0)

# Copying each alarm to the target region
alarm_batches = [response['MetricAlarms'][i:i+10] for i in range(0, len(response['MetricAlarms']), 10)]
for batch in alarm_batches:
    metric_alarms = []
    for alarm in batch:
        alarm_name = alarm['AlarmName']
        print('Copying alarm: ' + alarm_name)

        # Replacing SNS topic ARNs with the target region ARNs
        for action_type in ['OKActions', 'AlarmActions', 'InsufficientDataActions']:
            if action_type in alarm:
                for i in range(len(alarm[action_type])):
                    arn_parts = alarm[action_type][i].split(':')
                    arn_parts[3] = target_region
                    alarm[action_type][i] = ':'.join(arn_parts)

        # Removing existing instance state
        alarm.pop('StateValue', None)

        metric_alarms.append({
            'AlarmName': alarm_name,
            'AlarmDescription': alarm['AlarmDescription'],
            'ActionsEnabled': alarm['ActionsEnabled'],
            'OKActions': alarm['OKActions'],
            'AlarmActions': alarm['AlarmActions'],
            'InsufficientDataActions': alarm['InsufficientDataActions'],
            'MetricName': alarm['MetricName'],
            'Namespace': alarm['Namespace'],
            'Statistic': alarm['Statistic'],
            'Dimensions': alarm['Dimensions'],
            'Period': alarm['Period'],
            'EvaluationPeriods': alarm['EvaluationPeriods'],
            'ComparisonOperator': alarm['ComparisonOperator'],
            'Threshold': alarm['Threshold']
        })

    try:
        for alarm in metric_alarms:
            cloudwatch_target.put_metric_alarm(**alarm)
    except Exception as e:
        print(f"Error occurred while copying alarms to the target region: {e}")
        exit(1)

    print("All alarms have been successfully copied to the target region.")

# target_alarms = response['MetricAlarms']
# if len(target_alarms) == len(metric_alarms):
#     print("All alarms have been successfully copied to the target region.")
# else:
#     print("Some alarms were not copied to the target region.")
