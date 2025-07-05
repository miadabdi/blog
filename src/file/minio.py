import logging
import threading
from datetime import datetime, timedelta, timezone
from functools import lru_cache, wraps
from typing import Any, Dict, List

from minio import Minio
from minio.datatypes import PostPolicy
from minio.deleteobjects import DeleteObject
from minio.error import InvalidResponseError, S3Error
from minio.notificationconfig import (
    NotificationConfig,
    PrefixFilterRule,
    QueueConfig,
    SuffixFilterRule,
)

from ..common.exceptions.internal import InternalException
from ..common.exceptions.not_found import NotFoundException
from ..common.handle_sync import _handle_sync
from ..common.settings import settings

# Configure logging
logger = logging.getLogger(__name__)


class MinioServiceError(Exception):
    """Custom exception for MinIO service errors."""

    pass


class MinioService:
    """
    Service for interacting with MinIO storage.
    - Creates a Singleton instance of Minio client.
    - Ensures all required buckets exist at startup (no per-operation bucket existence checks).
    - Provides methods to create presigned URLs for file uploads and downloads.
        with limited expiration times and limited file size. saves into specified bucket
    - gets notified when file is uploaded directly into minio instance
    - provides methods to delete files from MinIO storage.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """Singleton pattern implementation."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(MinioService, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        endpoint: str | None,
        access_key: str | None,
        secret_key: str | None,
        secure: bool | None,
    ):
        """
        Initialize MinIO service.

        Args:
            endpoint: MinIO server endpoint
            access_key: Access key for MinIO
            secret_key: Secret key for MinIO
            secure: Use HTTPS if True, HTTP if False
            region: Region name
            bucket_names: List of bucket names to ensure exist
        """

        print("MINIO SERVICE CREATION")

        # Prevent re-initialization of singleton
        if hasattr(self, "_initialized"):
            return

        # Get configuration from environment variables if not provided
        self.endpoint = endpoint or f"{settings.MINIO_ENDPOINT}:{settings.MINIO_PORT}"
        self.access_key = access_key or settings.MINIO_ACCESS_KEY
        self.secret_key = secret_key or settings.MINIO_SECRET_KEY
        self.secure = secure or settings.MINIO_SECURE
        self.bucket_names = settings.MINIO_BUCKET_NAMES

        if not self.access_key or not self.secret_key:
            raise MinioServiceError("MinIO access key and secret key must be provided")

        try:
            # Initialize MinIO client
            self.client = Minio(
                endpoint=self.endpoint,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=self.secure,
            )

            # Test connection
            self.client.list_buckets()
            logger.info(f"Successfully connected to MinIO at {self.endpoint}")

        except Exception as e:
            logger.error(f"Failed to initialize MinIO client: {str(e)}")
            raise MinioServiceError(f"Failed to connect to MinIO: {str(e)}")

        # Ensure all buckets exist at startup
        if self.bucket_names:
            self.ensure_buckets_exist(self.bucket_names)

        self._initialized = True

    @staticmethod
    def _handle_minio_errors(func):
        """Decorator to handle MinIO errors consistently."""

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except S3Error as e:
                logger.error(f"MinIO S3 error in {func.__name__}: {e}")
                raise InternalException(message=f"Storage error: {e}")
            except InvalidResponseError as e:
                logger.error(f"MinIO invalid response in {func.__name__}: {e}")
                raise InternalException(message="Storage service error")
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {e}")
                raise InternalException(message="Internal server error")

        return wrapper

    @_handle_minio_errors
    def ensure_buckets_exist(self, bucket_names: List[str]) -> Dict[str, bool]:
        """
        Ensure that all specified buckets exist, create them if they don't.

        Args:
            bucket_names: List of bucket names to check/create

        Returns:
            Dict mapping bucket names to creation status (True if created, False if already existed)
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
        """Validate bucket name according to S3 naming rules."""
        if not bucket_name or len(bucket_name) < 3 or len(bucket_name) > 63:
            return False
        if bucket_name.startswith("-") or bucket_name.endswith("-"):
            return False
        if ".." in bucket_name or ".-" in bucket_name or "-." in bucket_name:
            return False
        return bucket_name.replace("-", "").replace(".", "").isalnum()

    @_handle_sync
    @_handle_minio_errors
    def create_presigned_upload_url(
        self,
        bucket_name: str,
        object_name: str,
        expires: timedelta = timedelta(hours=1),
        max_file_size: int = 10 * 1024 * 1024,  # 10MB default
    ) -> Dict[str, Any]:
        """
        Create a presigned URL for file upload with size and type restrictions.

        Args:
            bucket_name: Name of the bucket
            object_name: Name of the object to upload
            expires: URL expiration time
            max_file_size: Maximum allowed file size in bytes

        Returns:
            Dict containing presigned URL and upload conditions
        """
        # Convert to datetime by adding to current time
        expiration_time = datetime.now(timezone.utc) + expires

        # Create PostPolicy object
        policy = PostPolicy(bucket_name, expiration_time)
        policy.add_equals_condition("key", object_name)
        policy.add_content_length_range_condition(1, max_file_size)

        # if allowed_content_types:
        #     for content_type in allowed_content_types:
        #         policy.add_starts_with_condition(
        #             "content-type", content_type.split("/")[0]
        #         )

        try:
            presigned_post = self.client.presigned_post_policy(policy)

            logger.info(f"Created presigned upload URL for {bucket_name}/{object_name}")

            return {
                "bucket_name": bucket_name,
                "form_data": presigned_post,
            }

        except Exception as e:
            logger.error(f"Failed to create presigned upload URL: {e}")
            raise InternalException(message="Failed to create upload URL")

    @_handle_sync
    @_handle_minio_errors
    def create_presigned_download_url(
        self,
        bucket_name: str,
        object_name: str,
        expires: timedelta = timedelta(hours=1),
    ) -> Dict[str, Any]:
        """
        Create a presigned URL for file download.

        Args:
            bucket_name: Name of the bucket
            object_name: Name of the object to download
            expires: URL expiration time

        Returns:
            Dict containing presigned URL and metadata
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
                raise NotFoundException(resource="Object", resource_id=object_name)
            raise

    @_handle_sync
    @_handle_minio_errors
    def delete_file(self, bucket_name: str, object_name: str) -> bool:
        """
        Delete a file from MinIO storage.

        Args:
            bucket_name: Name of the bucket
            object_name: Name of the object to delete

        Returns:
            True if deletion was successful
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
    @_handle_minio_errors
    def delete_files(
        self, bucket_name: str, object_names: List[str]
    ) -> Dict[str, bool]:
        """
        Delete multiple files from MinIO storage.

        Args:
            bucket_name: Name of the bucket
            object_names: List of object names to delete

        Returns:
            Dict mapping object names to deletion status
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
    @_handle_minio_errors
    def setup_bucket_notification(
        self,
        bucket_name: str,
        queue_arn: str,
        events: List[str] | None = None,
        prefix: str = "",
        suffix: str = "",
    ) -> bool:
        """
        Setup bucket notification for file upload events.

        Args:
            bucket_name: Name of the bucket
            queue_arn: ARN of the notification queue (e.g., SQS, SNS)
            events: List of events to listen for
            prefix: Object key prefix filter
            suffix: Object key suffix filter

        Returns:
            True if notification was set up successfully
        """
        # Bucket existence is ensured at startup; no per-operation check needed

        if events is None:
            events = ["s3:ObjectCreated:*"]

        try:
            # Create filter rules
            prefix_rule = PrefixFilterRule(prefix) if prefix else None
            suffix_rule = SuffixFilterRule(suffix) if suffix else None

            # Create notification configuration
            queue_config = QueueConfig(
                queue_arn,
                events,
                config_id="upload-notification",
                prefix_filter_rule=prefix_rule,
                suffix_filter_rule=suffix_rule,
            )

            notification_config = NotificationConfig(queue_config_list=[queue_config])

            self.client.set_bucket_notification(bucket_name, notification_config)
            logger.info(f"Set up notification for bucket {bucket_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to set up bucket notification: {e}")
            return False

    @_handle_sync
    @_handle_minio_errors
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
            bucket_name: Name of the bucket
            prefix: Object key prefix filter
            recursive: List objects recursively
            max_objects: Maximum number of objects to return

        Returns:
            List of object information dictionaries
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
    @_handle_minio_errors
    def get_object_info(self, bucket_name: str, object_name: str) -> Dict[str, Any]:
        """
        Get detailed information about an object.

        Args:
            bucket_name: Name of the bucket
            object_name: Name of the object

        Returns:
            Dictionary containing object metadata
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
                raise NotFoundException(
                    resource="Object",
                    resource_id=object_name,
                )
            raise

    @_handle_sync
    @_handle_minio_errors
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the MinIO service.

        Returns:
            Dictionary containing health status information
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
    @_handle_minio_errors
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
        NOTE: Content-type and file size restrictions are NOT enforced by MinIO/S3 for PUT URLs.
        You must validate these after upload.
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
def get_MinioService(
    endpoint: str | None = None,
    access_key: str | None = None,
    secret_key: str | None = None,
    secure: bool | None = None,
) -> MinioService:
    """
    Factory function to get MinioService instance.
    Can be used as a FastAPI dependency.
    """
    return MinioService(
        endpoint=endpoint, access_key=access_key, secret_key=secret_key, secure=secure
    )
