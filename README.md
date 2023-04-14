
# Copy Cloudwatch alarms and SNS Topics from region to another
This Python script is designed to copy CloudWatch alarms and SNS topics from one AWS region to another using the Boto3 library.

### Requirements
The following packages are required to run this script:

    dotenv
    boto3

You can install these packages using the following command, I highly recommend to use a virtual environment before installing requirements :

    pip install -r requirements.txt

### Usage
To use this script, you will need to set up your AWS credentials and configure your environment variables in a .env file.

The .env file should contain the following variables:

    SOURCE_REGION: The source region where you want to copy the CloudWatch alarms and SNS topics from.
    TARGET_REGION: Your AWS secret access key.
    AWS_ACCESS_KEY_ID: The destination region where you want to copy the resources to.
    AWS_SECRET_ACCESS_KEY: Your AWS access key ID.

#### Once you have set up your environment variables, you can run the script using the following command:

    python cloudwatch.py or python cloudwatch_sns.py

### Note
Please note that this script will copy all CloudWatch alarms and SNS topics from the source region to the destination region. If you only want to copy specific alarms or topics, you will need to modify the script accordingly.


