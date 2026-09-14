"""
Service layer for file operations using S3-compatible storage.
Handles business logic for uploads, object streaming, and presigned URLs.
"""

import uuid
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, UploadFile

from ..common.exceptions.exceptions import EntityNotFoundException
from ..common.settings import settings
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

    async def upload_file(self, file: UploadFile, bucket_name: str) -> dict:
        """
        Store an uploaded file in the given bucket.

        Args:
            file (UploadFile): The uploaded file.
            bucket_name (str): Target bucket (must be a configured bucket).

        Returns:
            dict: Stored object metadata.

        Raises:
            EntityNotFoundException: If the bucket is not a configured bucket.
        """
        if bucket_name not in settings.S3_BUCKET_NAMES:
            raise EntityNotFoundException(resource="Bucket", resource_id=bucket_name)

        object_name = self._generate_unique_object_name(file.filename or "upload")
        return await self.minio.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_stream=file.file,
            length=file.size,
            content_type=file.content_type,
        )

    async def open_object(self, bucket_name: str, object_name: str):
        """
        Open a stored object for streaming.

        Args:
            bucket_name (str): The bucket name.
            object_name (str): The object name.

        Returns:
            tuple: (response stream, stat metadata).
        """
        return await self.minio.get_object_stream(
            bucket_name=bucket_name, object_name=object_name
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
