import os
from minio import Minio
from dotenv import load_dotenv

load_dotenv()

MINIO_CLIENT = Minio(
    endpoint="localhost:9000",
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False,
)

BUCKET_NAME = "media"

def initialize_minio_bucket():
    
    try:
        if not MINIO_CLIENT.bucket_exists(BUCKET_NAME):
            MINIO_CLIENT.make_bucket(BUCKET_NAME)
            print(f"Bucket '{BUCKET_NAME}' created successfully.")
        else:
            print(f"Bucket '{BUCKET_NAME}' already exists.")
    except Exception as e:
        print(f"Warning: Could not initialize MinIO bucket. Reason: {e}")
