


from fastapi import UploadFile
from user_management.minio.config import MINIO_CLIENT, BUCKET_NAME

async def upload_to_minio(file: UploadFile, folder: str):
    file_name = f"{folder}/{file.filename}"
    MINIO_CLIENT.put_object(
        bucket_name=BUCKET_NAME,
        object_name=file_name,
        data=file.file,
        length=-1,
        part_size=10 * 1024 * 1024,  # 10MB chunk size
        content_type=file.content_type
    )
    return f"http://localhost:9000/{BUCKET_NAME}/{file_name}"
