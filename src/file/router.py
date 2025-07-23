"""
API router for file operations.
Handles HTTP endpoints for generating presigned upload and download URLs.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from ..auth.auth import authorize, get_current_user
from ..auth.models import User
from ..common.user_role import UserRole
from .service import FileService, get_FileService

router = APIRouter(prefix="/file", tags=["file"])


@router.get("/image-upload-url")
@authorize(role=[UserRole.ADMIN])
async def get_image_upload_url(
    current_user: Annotated[User, Depends(get_current_user)],
    uploadname: str = Query(..., description="Original filename"),
    expires_seconds: int = Query(3600, description="URL expiry in seconds"),
    file_service: FileService = Depends(get_FileService),
):
    """
    Generate a presigned URL for uploading an image.

    Args:
        current_user (User): The current authenticated user.
        uploadname (str): The original filename.
        expires_seconds (int): URL expiry in seconds.
        file_service (FileService): The file service dependency.

    Returns:
        dict: Presigned URL and form data for image upload.
    """
    return await file_service.create_image_upload_url(uploadname, expires_seconds)


@router.get("/file-upload-url")
@authorize(role=[UserRole.ADMIN])
async def get_file_upload_url(
    current_user: Annotated[User, Depends(get_current_user)],
    uploadname: str = Query(..., description="Original filename"),
    expires_seconds: int = Query(3600, description="URL expiry in seconds"),
    file_service: FileService = Depends(get_FileService),
):
    """
    Generate a presigned URL for uploading a general file.

    Args:
        current_user (User): The current authenticated user.
        uploadname (str): The original filename.
        expires_seconds (int): URL expiry in seconds.
        file_service (FileService): The file service dependency.

    Returns:
        dict: Presigned URL and form data for file upload.
    """
    return await file_service.create_file_upload_url(uploadname, expires_seconds)


@router.get("/download-url")
async def get_download_url(
    bucket_name: str = Query(..., description="Bucket name"),
    object_name: str = Query(..., description="Object name"),
    expires_seconds: int = Query(3600, description="URL expiry in seconds"),
    file_service: FileService = Depends(get_FileService),
):
    """
    Generate a presigned URL for downloading a file.

    Args:
        bucket_name (str): The bucket name.
        object_name (str): The object name.
        expires_seconds (int): URL expiry in seconds.
        file_service (FileService): The file service dependency.

    Returns:
        dict: Presigned download URL and metadata.
    """
    return await file_service.create_download_url(
        bucket_name, object_name, expires_seconds
    )
