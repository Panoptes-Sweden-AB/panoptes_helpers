import boto3
import psycopg2
from psycopg2.extras import RealDictCursor

def client(region, db_name, workgroup_name, aws_access_key_id, aws_secret_access_key):
    # Fetch AWS credentials from environment variables

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("Missing AWS credentials in environment variables")

    # Create session with credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )

    # Step 1: Get workgroup endpoint
    rs = session.client('redshift-serverless')
    workgroup = rs.get_workgroup(workgroupName=workgroup_name)['workgroup']
    host = workgroup['endpoint']['address']
    port = workgroup['endpoint']['port']

    # Step 2: Get IAM-based temporary credentials
    creds = rs.get_credentials(
        workgroupName=workgroup_name,
        durationSeconds=900
    )

    # Step 3: Connect using psycopg2
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=db_name,
        user=creds['dbUser'],
        password=creds['dbPassword'],
        cursor_factory=RealDictCursor
    )
    return conn
