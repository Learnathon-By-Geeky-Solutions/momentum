import os
from minio import Minio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MINIO_CLIENT = Minio(
    endpoint="localhost:9000",  # MinIO URL
    access_key=os.getenv("MINIO_ACCESS_KEY"), 
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False  # Set to True if using HTTPS
)

BUCKET_NAME = "media"

# Ensure the bucket exists
if not MINIO_CLIENT.bucket_exists(BUCKET_NAME):
    MINIO_CLIENT.make_bucket(BUCKET_NAME)
    print(f"Bucket '{BUCKET_NAME}' created successfully.")
else:
    print(f"Bucket '{BUCKET_NAME}' already exists.")
