import uuid
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from .minio import MinioService, get_MinioService


class FileService:
    def __init__(self, minio: MinioService):
        self.minio = minio

    def _generate_unique_object_name(self, uploadname: str) -> str:
        """
        Generate a unique object name using the uploadname, current timestamp, and a random UUID.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        unique_suffix = uuid.uuid4().hex[:8]
        return f"{timestamp}_{unique_suffix}_{uploadname}"

    async def create_image_upload_url(
        self, uploadname: str, expires_seconds: int = 3600
    ) -> dict:
        """
        Create a presigned URL for uploading an image to the 'images' bucket (max 10MB).
        """
        object_name = self._generate_unique_object_name(uploadname)
        return await self.minio.create_presigned_upload_url(
            bucket_name="images",
            object_name=object_name,
            expires=timedelta(seconds=expires_seconds),
            max_file_size=10 * 1024 * 1024,  # 10MB
            # allowed_content_types=["image/"],
        )

    async def create_file_upload_url(
        self, uploadname: str, expires_seconds: int = 3600
    ) -> dict:
        """
        Create a presigned URL for uploading a general file to the 'files' bucket (max 100MB, disallow images).
        """
        object_name = self._generate_unique_object_name(uploadname)
        return await self.minio.create_presigned_upload_url(
            bucket_name="files",
            object_name=object_name,
            expires=timedelta(seconds=expires_seconds),
            max_file_size=100 * 1024 * 1024,  # 100MB
            # allowed_content_types=["application/", "text/"],
        )

    async def create_download_url(
        self, bucket_name: str, object_name: str, expires_seconds: int = 3600
    ) -> dict:
        """
        Create a presigned URL for downloading a file from the specified bucket.
        """
        return await self.minio.create_presigned_download_url(
            bucket_name=bucket_name,
            object_name=object_name,
            expires=timedelta(seconds=expires_seconds),
        )


@lru_cache
def get_FileService(
    categoryRepository: Annotated[MinioService, Depends(get_MinioService)],
) -> FileService:
    return FileService(categoryRepository)
