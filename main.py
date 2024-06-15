import boto3
import pymysql
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Initialize clients
s3_client = boto3.client('s3')
glue_client = boto3.client('glue')

def read_from_s3(bucket_name, file_key):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        data = response['Body'].read().decode('utf-8')
        return data
    except Exception as e:
        print(f"Error reading from S3: {e}")
        return None

def push_to_rds(data):
    try:
        # Replace with your RDS connection details
        rds_client = pymysql.connect(
            host='database-1.ct6sya4y0gq9.us-east-1.rds.amazonaws.com',
            user='admin',
            password='Pass1234',
            database='practical'
        )
        with rds_client.cursor() as cursor:
            sql = "INSERT INTO demo (id, name, email) VALUES (%s)"
            cursor.execute(sql, (data,))
            rds_client.commit()
    except Exception as e:
        print(f"Error pushing to RDS: {e}")
        return False
    return True

def push_to_glue(data):
    try:
        # Example Glue API call, modify as needed
        glue_client.put_record(
            DatabaseName='practical-demo',
            TableName='demo-table',
            Record={'': data}
        )
    except Exception as e:
        print(f"Error pushing to Glue: {e}")

def main():
    bucket_name = 'practial-bucket'
    file_key = 'your-file-key'
    
    data = read_from_s3(bucket_name, file_key)
    if data:
        success = push_to_rds(data)
        if not success:
            push_to_glue(data)

if __name__ == "__main__":
    main()

