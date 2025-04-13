from fastapi import UploadFile, HTTPException
from typing import List, Tuple, Optional
from app.models import Product
from fastapi import UploadFile
from app.minio.config import MINIO_CLIENT, BUCKET_NAME
from minio.error import S3Error
from urllib.parse import urlparse
from typing import List

PRODUCT_PHOTO = "product photo"
PRODUCT_VIDEO = "product video"

VALID_TYPES = ["profile", PRODUCT_PHOTO, PRODUCT_VIDEO]
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
        content_type=file.content_type,
    )
    return f"http://localhost:9000/{BUCKET_NAME}/{file_name}"


def validate_file_type(content_type: str, upload_type: str) -> None:
    if upload_type in ["profile", PRODUCT_PHOTO]:
        if content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {content_type}. Only JPEG and PNG images are allowed.",
            )
    elif upload_type == PRODUCT_VIDEO:
        if content_type not in ALLOWED_VIDEO_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {content_type}. Only MP4 and MPEG videos are allowed.",
            )


def validate_file_size(file_size: int) -> None:
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400, detail=f"File size should not exceed {MAX_FILE_SIZE_MB}MB"
        )


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


def validate_files(files: List[UploadFile], file_type: str):
    for file in files:
        content_type = file.content_type
        contents = file.file.read()
        file_size = len(contents)
        file.file.seek(0)

        if (
            file_type in ["profile", PRODUCT_PHOTO]
            and content_type not in ALLOWED_IMAGE_TYPES
        ):
            raise HTTPException(
                status_code=400, detail=f"Invalid image file type: {content_type}"
            )
        if file_type == PRODUCT_VIDEO and content_type not in ALLOWED_VIDEO_TYPES:
            raise HTTPException(
                status_code=400, detail=f"Invalid video file type: {content_type}"
            )
        if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=400, detail=f"File size exceeds {MAX_FILE_SIZE_MB}MB"
            )


def get_folder_for_type(upload_type: str) -> str:
    if upload_type == "profile":
        return "profile"
    if upload_type == PRODUCT_PHOTO:
        return "photos"
    return "videos"


def find_product_and_url(
    products: List[Product], product_field: str, file_name: str
) -> Tuple[Optional[Product], Optional[str]]:
    for product in products:
        file_urls = getattr(product, product_field, [])
        for url in file_urls:
            if file_name in url:
                return product, url
    return None, None
