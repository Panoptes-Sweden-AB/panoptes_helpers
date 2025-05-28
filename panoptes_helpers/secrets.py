import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name, region_name, aws_access_key_id, aws_secret_access_key):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,  # Use default credentials
        aws_secret_access_key=aws_secret_access_key  # Use default credentials
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return secret
