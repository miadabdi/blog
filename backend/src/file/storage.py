"""
StorageService: S3-compatible object storage via the minio client library (SeaweedFS, MinIO, AWS S3).
Provides methods for bucket management, presigned URL generation, file deletion, and health checks.
"""

import logging
import threading
from datetime import datetime, timedelta, timezone
from functools import lru_cache, wraps
from typing import Any, Dict, List

from minio import Minio
from minio.deleteobjects import DeleteObject
from minio.error import InvalidResponseError, S3Error

from ..common.exceptions.exceptions import EntityNotFoundException, InternalException
from ..common.handle_sync import _handle_sync
from ..common.settings import settings

# Configure logging
logger = logging.getLogger(__name__)


class StorageServiceError(Exception):
    """Custom exception for storage service errors."""

    pass


class StorageService:
    """
    S3-compatible object storage via the minio client library.

    - Singleton pattern for Minio client.
    - Ensures all required buckets exist at startup.
    - Provides methods to create presigned URLs for file uploads and downloads.
    - Provides presigned URL generation and deletion utilities.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """Singleton pattern implementation."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(StorageService, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        endpoint: str | None,
        access_key: str | None,
        secret_key: str | None,
        secure: bool | None,
    ):
        """
        Initialize storage service.

        Args:
            endpoint (str | None): S3 server endpoint.
            access_key (str | None): Access key.
            secret_key (str | None): Secret key.
            secure (bool | None): Use HTTPS if True, HTTP if False.

        Raises:
            StorageServiceError: If credentials are missing or connection fails.
        """


        # Prevent re-initialization of singleton
        if hasattr(self, "_initialized"):
            return

        # Get configuration from environment variables if not provided
        self.endpoint = endpoint or f"{settings.S3_ENDPOINT}:{settings.S3_PORT}"
        self.access_key = access_key or settings.S3_ACCESS_KEY
        self.secret_key = secret_key or settings.S3_SECRET_KEY
        self.secure = secure or settings.S3_SECURE
        self.bucket_names = settings.S3_BUCKET_NAMES

        if not self.access_key or not self.secret_key:
            raise StorageServiceError("S3 access key and secret key must be provided")

        try:
            # Initialize S3 client
            self.client = Minio(
                endpoint=self.endpoint,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=self.secure,
            )

            # Test connection
            self.client.list_buckets()
            logger.info(f"Successfully connected to S3 storage at {self.endpoint}")

        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {str(e)}")
            raise StorageServiceError(f"Failed to connect to storage: {str(e)}")

        # Ensure all buckets exist at startup
        if self.bucket_names:
            self.ensure_buckets_exist(self.bucket_names)

        self._initialized = True

    @staticmethod
    def _handle_storage_errors(func):
        """Decorator to handle storage errors consistently."""

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except S3Error as e:
                logger.error(f"S3 error in {func.__name__}: {e}")
                raise InternalException(message=f"Storage error: {e}")
            except InvalidResponseError as e:
                logger.error(f"Invalid S3 response in {func.__name__}: {e}")
                raise InternalException(message="Storage service error")
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {e}")
                raise InternalException(message="Internal server error")

        return wrapper

    @_handle_storage_errors
    def ensure_buckets_exist(self, bucket_names: List[str]) -> Dict[str, bool]:
        """
        Ensure that all specified buckets exist, create them if they don't.

        Args:
            bucket_names (List[str]): List of bucket names to check/create.

        Returns:
            Dict[str, bool]: Mapping bucket names to creation status (True if created, False if already existed).
        """
        results = {}

        for bucket_name in bucket_names:
            if not self._is_valid_bucket_name(bucket_name):
                logger.warning(f"Invalid bucket name: {bucket_name}")
                results[bucket_name] = False
                continue

            try:
                if not self.client.bucket_exists(bucket_name):
                    self.client.make_bucket(bucket_name)
                    logger.info(f"Created bucket: {bucket_name}")
                    results[bucket_name] = True
                else:
                    logger.info(f"Bucket already exists: {bucket_name}")
                    results[bucket_name] = False

            except Exception as e:
                logger.error(f"Failed to create bucket {bucket_name}: {e}")
                results[bucket_name] = False

        return results

    def _is_valid_bucket_name(self, bucket_name: str) -> bool:
        """
        Validate bucket name according to S3 naming rules.

        Args:
            bucket_name (str): The bucket name.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not bucket_name or len(bucket_name) < 3 or len(bucket_name) > 63:
            return False
        if bucket_name.startswith("-") or bucket_name.endswith("-"):
            return False
        if ".." in bucket_name or ".-" in bucket_name or "-." in bucket_name:
            return False
        return bucket_name.replace("-", "").replace(".", "").isalnum()

    @_handle_sync
    @_handle_storage_errors
    def create_presigned_download_url(
        self,
        bucket_name: str,
        object_name: str,
        expires: timedelta = timedelta(hours=1),
    ) -> Dict[str, Any]:
        """
        Create a presigned URL for file download.

        Args:
            bucket_name (str): Name of the bucket.
            object_name (str): Name of the object to download.
            expires (timedelta): URL expiration time.

        Returns:
            Dict[str, Any]: Presigned download URL and metadata.

        Raises:
            EntityNotFoundException: If the object does not exist.
        """
        # Bucket existence is ensured at startup; no per-operation check needed

        try:
            # Check if object exists
            self.client.stat_object(bucket_name, object_name)

            presigned_url = self.client.presigned_get_object(
                bucket_name=bucket_name, object_name=object_name, expires=expires
            )

            logger.info(
                f"Created presigned download URL for {bucket_name}/{object_name}"
            )

            return {
                "url": presigned_url,
                "expires_in_seconds": int(expires.total_seconds()),
                "object_name": object_name,
                "bucket_name": bucket_name,
            }

        except S3Error as e:
            if e.code == "NoSuchKey":
                raise EntityNotFoundException(
                    resource="Object", resource_id=object_name
                )
            raise

    @_handle_sync
    @_handle_storage_errors
    def delete_file(self, bucket_name: str, object_name: str) -> bool:
        """
        Delete a file from S3 storage.

        Args:
            bucket_name (str): Name of the bucket.
            object_name (str): Name of the object to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        # Bucket existence is ensured at startup; no per-operation check needed

        try:
            # Check if object exists before attempting deletion
            self.client.stat_object(bucket_name, object_name)

            self.client.remove_object(bucket_name, object_name)
            logger.info(f"Successfully deleted {bucket_name}/{object_name}")
            return True

        except S3Error as e:
            if e.code == "NoSuchKey":
                logger.warning(f"Object {bucket_name}/{object_name} does not exist")
                return False
            raise

    @_handle_sync
    @_handle_storage_errors
    def delete_files(
        self, bucket_name: str, object_names: List[str]
    ) -> Dict[str, bool]:
        """
        Delete multiple files from MinIO storage.

        Args:
            bucket_name (str): Name of the bucket.
            object_names (List[str]): List of object names to delete.

        Returns:
            Dict[str, bool]: Mapping object names to deletion status.
        """
        # Bucket existence is ensured at startup; no per-operation check needed

        results = {}

        try:
            # Convert strings to DeleteObject instances
            delete_object_list = [DeleteObject(obj_name) for obj_name in object_names]
            errors = self.client.remove_objects(bucket_name, delete_object_list)

            # Initialize all as successful
            for obj_name in object_names:
                results[obj_name] = True

            # Handle any errors - errors is an iterator of DeleteError objects
            for error in errors:
                # DeleteError has 'object_name' attribute
                results[error.name] = False
                logger.error(f"Failed to delete {error.name}: {error}")

            logger.info(f"Bulk delete completed for bucket {bucket_name}")
            return results

        except Exception as e:
            logger.error(f"Bulk delete failed: {e}")
            # Return False for all objects if bulk operation fails
            return {obj_name: False for obj_name in object_names}

    @_handle_sync
    @_handle_storage_errors
    def list_objects(
        self,
        bucket_name: str,
        prefix: str = "",
        recursive: bool = True,
        max_objects: int = 1000,
    ) -> List[Dict[str, Any]]:
        """
        List objects in a bucket.

        Args:
            bucket_name (str): Name of the bucket.
            prefix (str): Object key prefix filter.
            recursive (bool): List objects recursively.
            max_objects (int): Maximum number of objects to return.

        Returns:
            List[Dict[str, Any]]: List of object information dictionaries.

        Raises:
            InternalException: If listing fails.
        """
        # Bucket existence is ensured at startup; no per-operation check needed

        try:
            objects = []
            count = 0

            for obj in self.client.list_objects(
                bucket_name, prefix=prefix, recursive=recursive
            ):
                if count >= max_objects:
                    break

                objects.append(
                    {
                        "object_name": obj.object_name,
                        "size": obj.size,
                        "etag": obj.etag,
                        "last_modified": obj.last_modified.isoformat()
                        if obj.last_modified
                        else None,
                        "content_type": obj.content_type,
                    }
                )
                count += 1

            logger.info(f"Listed {len(objects)} objects from bucket {bucket_name}")
            return objects

        except Exception as e:
            logger.error(f"Failed to list objects: {e}")
            raise InternalException(message="Failed to list objects")

    @_handle_sync
    @_handle_storage_errors
    def get_object_info(self, bucket_name: str, object_name: str) -> Dict[str, Any]:
        """
        Get detailed information about an object.

        Args:
            bucket_name (str): Name of the bucket.
            object_name (str): Name of the object.

        Returns:
            Dict[str, Any]: Object metadata.

        Raises:
            EntityNotFoundException: If the object does not exist.
        """
        # Bucket existence is ensured at startup; no per-operation check needed

        try:
            stat = self.client.stat_object(bucket_name, object_name)

            return {
                "object_name": stat.object_name,
                "size": stat.size,
                "etag": stat.etag,
                "last_modified": stat.last_modified.isoformat()
                if stat.last_modified
                else None,
                "content_type": stat.content_type,
                "metadata": stat.metadata,
                "bucket_name": bucket_name,
            }

        except S3Error as e:
            if e.code == "NoSuchKey":
                raise EntityNotFoundException(
                    resource="Object",
                    resource_id=object_name,
                )
            raise

    @_handle_sync
    @_handle_storage_errors
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the MinIO service.

        Returns:
            Dict[str, Any]: Health status information.
        """
        try:
            # Test connection by listing buckets
            buckets = self.client.list_buckets()

            return {
                "status": "healthy",
                "endpoint": self.endpoint,
                "buckets_count": len(buckets),
                "secure": self.secure,
            }

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "endpoint": self.endpoint,
                "error": str(e),
                "secure": self.secure,
            }

    @_handle_sync
    @_handle_storage_errors
    def put_object(
        self,
        bucket_name: str,
        object_name: str,
        file_stream,
        length: int,
        content_type: str | None = None,
    ) -> Dict[str, Any]:
        """
        Store an object from a file stream.

        Args:
            bucket_name (str): Name of the bucket.
            object_name (str): Name of the object.
            file_stream: Binary stream of the file content.
            length (int): Size of the content in bytes.
            content_type (str | None): MIME type of the content.

        Returns:
            Dict[str, Any]: Stored object metadata.
        """
        self.client.put_object(
            bucket_name,
            object_name,
            file_stream,
            length,
            content_type=content_type or "application/octet-stream",
        )
        stat = self.client.stat_object(bucket_name, object_name)
        return {
            "object_name": object_name,
            "bucket_name": bucket_name,
            "content_type": stat.content_type,
            "size": stat.size,
        }

    @_handle_sync
    @_handle_storage_errors
    def get_object_stream(self, bucket_name: str, object_name: str):
        """
        Open an object for streaming.

        Args:
            bucket_name (str): Name of the bucket.
            object_name (str): Name of the object.

        Returns:
            tuple: (response stream, stat metadata).

        Raises:
            EntityNotFoundException: If the object does not exist.
        """
        stat = self.client.stat_object(bucket_name, object_name)
        return self.client.get_object(bucket_name, object_name), stat

    @_handle_sync
    @_handle_storage_errors
    def create_presigned_put_upload_url(
        self,
        bucket_name: str,
        object_name: str,
        expires: timedelta = timedelta(hours=1),
        allowed_content_types: list[str] | None = None,
        max_file_size: int | None = None,
    ) -> dict:
        """
        Create a presigned PUT URL for file upload.

        Args:
            bucket_name (str): Name of the bucket.
            object_name (str): Name of the object to upload.
            expires (timedelta): URL expiration time.
            allowed_content_types (list[str] | None): Allowed content types (not enforced).
            max_file_size (int | None): Maximum file size (not enforced).

        Returns:
            dict: Presigned PUT URL and metadata.

        Raises:
            InternalException: If URL creation fails.
        """
        # Bucket existence is ensured at startup; no per-operation check needed

        try:
            url = self.client.presigned_put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                expires=expires,
            )
            return {
                "url": url,
                "expires_in_seconds": int(expires.total_seconds()),
                "note": (
                    "Content-type and file size restrictions are NOT enforced by this URL. "
                    "You must validate after upload."
                ),
                "allowed_content_types": allowed_content_types,
                "max_file_size": max_file_size,
            }

        except Exception as e:
            logger.error(f"Failed to create presigned PUT upload URL: {e}")
            raise InternalException(message="Failed to create upload URL")


# Factory function for dependency injection in FastAPI
@lru_cache
def get_StorageService(
    endpoint: str | None = None,
    access_key: str | None = None,
    secret_key: str | None = None,
    secure: bool | None = None,
) -> StorageService:
    """
    Factory function to get StorageService instance.
    Can be used as a FastAPI dependency.

    Args:
        endpoint (str | None): S3 server endpoint.
        access_key (str | None): Access key.
        secret_key (str | None): Secret key.
        secure (bool | None): Use HTTPS if True, HTTP if False.

    Returns:
        StorageService: The StorageService singleton instance.
    """
    return StorageService(
        endpoint=endpoint, access_key=access_key, secret_key=secret_key, secure=secure
    )
