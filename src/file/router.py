from typing import Annotated

from fastapi import APIRouter, Depends, Query

from ..auth.auth import authorize, get_current_user
from ..auth.models import User
from ..common.user_role import UserRole
from .service import FileService, get_FileService

router = APIRouter(prefix="/file", tags=["file"])


@router.get("/image-upload-url")
@authorize(role=[UserRole.ADMIN])
def get_image_upload_url(
    current_user: Annotated[User, Depends(get_current_user)],
    uploadname: str = Query(..., description="Original filename"),
    expires_seconds: int = Query(3600, description="URL expiry in seconds"),
    file_service: FileService = Depends(get_FileService),
):
    return file_service.create_image_upload_url(uploadname, expires_seconds)


@router.get("/file-upload-url")
@authorize(role=[UserRole.ADMIN])
def get_file_upload_url(
    current_user: Annotated[User, Depends(get_current_user)],
    uploadname: str = Query(..., description="Original filename"),
    expires_seconds: int = Query(3600, description="URL expiry in seconds"),
    file_service: FileService = Depends(get_FileService),
):
    return file_service.create_file_upload_url(uploadname, expires_seconds)


@router.get("/download-url")
def get_download_url(
    bucket_name: str = Query(..., description="Bucket name"),
    object_name: str = Query(..., description="Object name"),
    expires_seconds: int = Query(3600, description="URL expiry in seconds"),
    file_service: FileService = Depends(get_FileService),
):
    return file_service.create_download_url(bucket_name, object_name, expires_seconds)
