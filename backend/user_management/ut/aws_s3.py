

import os
from fastapi import UploadFile
from dotenv import load_dotenv
import boto3

# Load AWS credentials
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_REGION = os.getenv("S3_REGION")

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=S3_REGION
)


def upload_files_to_s3(files: list[UploadFile], folder: str):
    """
    Upload multiple files to AWS S3 and return their URLs.
    """
    file_urls = []

    for file in files:
        file_extension = file.filename.split(".")[-1]
        s3_filename = f"{folder}/{file.filename}"

        # Upload file to S3
        s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, s3_filename, ExtraArgs={"ACL": "public-read"})

        # Generate URL
        file_url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{s3_filename}"
        file_urls.append(file_url)

    return file_urls
