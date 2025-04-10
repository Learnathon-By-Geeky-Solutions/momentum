
from fastapi import UploadFile, HTTPException

from fastapi import UploadFile
from user_management.minio.config import MINIO_CLIENT, BUCKET_NAME
from minio.error import S3Error
from urllib.parse import urlparse





VALID_TYPES = ["profile", "product photo", "product video"]
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
ALLOWED_VIDEO_TYPES = ["video/mp4", "video/mpeg"]
MAX_FILE_SIZE_MB = 5  # 5 MB

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



def validate_file_type(content_type: str, upload_type: str) -> None:
    if upload_type in ["profile", "product photo"]:
        if content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid file type: {content_type}. Only JPEG and PNG images are allowed.")
    elif upload_type == "product video":
        if content_type not in ALLOWED_VIDEO_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid file type: {content_type}. Only MP4 and MPEG videos are allowed.")



def validate_file_size(file_size: int) -> None:
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File size should not exceed {MAX_FILE_SIZE_MB}MB")



async def delete_from_minio(object_name: str) -> bool:
    try:
        found = MINIO_CLIENT.stat_object(BUCKET_NAME, object_name)
        if found:
            MINIO_CLIENT.remove_object(BUCKET_NAME, object_name)
            return True
    except S3Error as e:
        print(f"Error deleting file: {e}")
        return False
    
    
def extract_minio_object_key(url: str) -> str:
    """
    Converts 'http://localhost:9000/media/photos/007.jpg' → 'photos/007.jpg'
    """
    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/", 2)
    if len(parts) >= 2:
        return "/".join(parts[1:])  # Skip the bucket name
    return parts[-1]