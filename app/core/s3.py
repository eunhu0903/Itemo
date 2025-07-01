import os
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
BUCKET_NAME = os.getenv('BUCKET_NAME')

if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, BUCKET_NAME]):
    logger.error("AWS 환경 변수 중 일부가 설정되어 있지 않습니다.")

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

def upload_fileobj(file_obj, object_name: str, bucket_name: str = BUCKET_NAME) -> str | None:
    try:
        s3_client.upload_fileobj(
            Fileobj=file_obj,
            Bucket=bucket_name,
            Key=object_name,
        )
        url = f"https://{bucket_name}.s3.{AWS_REGION}.amazonaws.com/{object_name}"
        return url
    except ClientError as e:
        logger.error(f"S3 Upload error: {e}")
        return None

def delete_object(bucket_name: str, object_name: str) -> bool:
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)
        return True
    except ClientError as e:
        logger.error(f"S3 Delete error: {e}")
        return False
