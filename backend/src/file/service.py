"""
Service layer for file operations using MinIO.
Handles business logic for generating presigned URLs for uploads and downloads.
"""

import uuid
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from .storage import StorageService, get_StorageService


class FileService:
    """
    Service class for managing file operations via S3-compatible storage.
    """

    def __init__(self, minio: StorageService):
        """
        Initialize FileService with a StorageService instance.

        Args:
            minio (StorageService): The StorageService instance.
        """
        self.minio = minio

    def _generate_unique_object_name(self, uploadname: str) -> str:
        """
        Generate a unique object name using the uploadname, current timestamp, and a random UUID.

        Args:
            uploadname (str): The original filename.

        Returns:
            str: A unique object name for storage.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        unique_suffix = uuid.uuid4().hex[:8]
        return f"{timestamp}_{unique_suffix}_{uploadname}"

    async def create_image_upload_url(
        self, uploadname: str, expires_seconds: int = 3600
    ) -> dict:
        """
        Create a presigned PUT URL for uploading an image to the 'images' bucket (max 10MB).

        Args:
            uploadname (str): The original filename.
            expires_seconds (int): Expiry time for the URL in seconds.

        Returns:
            dict: Presigned PUT URL and metadata for upload.
        """
        object_name = self._generate_unique_object_name(uploadname)
        return await self.minio.create_presigned_put_upload_url(
            bucket_name="images",
            object_name=object_name,
            expires=timedelta(seconds=expires_seconds),
            max_file_size=10 * 1024 * 1024,  # 10MB (documented; not enforced by the URL)
        )

    async def create_file_upload_url(
        self, uploadname: str, expires_seconds: int = 3600
    ) -> dict:
        """
        Create a presigned PUT URL for uploading a general file to the 'files' bucket (max 100MB).

        Args:
            uploadname (str): The original filename.
            expires_seconds (int): Expiry time for the URL in seconds.

        Returns:
            dict: Presigned PUT URL and metadata for upload.
        """
        object_name = self._generate_unique_object_name(uploadname)
        return await self.minio.create_presigned_put_upload_url(
            bucket_name="files",
            object_name=object_name,
            expires=timedelta(seconds=expires_seconds),
            max_file_size=100 * 1024 * 1024,  # 100MB (documented; not enforced by the URL)
        )

    async def create_download_url(
        self, bucket_name: str, object_name: str, expires_seconds: int = 3600
    ) -> dict:
        """
        Create a presigned URL for downloading a file from the specified bucket.

        Args:
            bucket_name (str): The bucket name.
            object_name (str): The object name.
            expires_seconds (int): Expiry time for the URL in seconds.

        Returns:
            dict: Presigned download URL and metadata.
        """
        return await self.minio.create_presigned_download_url(
            bucket_name=bucket_name,
            object_name=object_name,
            expires=timedelta(seconds=expires_seconds),
        )


@lru_cache
def get_FileService(
    categoryRepository: Annotated[StorageService, Depends(get_StorageService)],
) -> FileService:
    """
    Dependency injector for FileService.

    Args:
        categoryRepository (StorageService): The StorageService instance.

    Returns:
        FileService: The FileService instance.
    """
    return FileService(categoryRepository)
