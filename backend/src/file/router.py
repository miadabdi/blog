"""
API router for file operations.
Handles HTTP endpoints for file uploads, object streaming, and presigned URLs.
"""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    Query,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import StreamingResponse

from ..auth.auth import authorize, get_current_user
from ..auth.models import User
from ..common.http_responses.doc_responses import (
    ResponseErrorDoc,
    ResponseSuccessDoc,
)
from ..common.http_responses.success_response import SuccessCodes
from ..common.http_responses.success_result import SuccessResult
from ..common.user_role import UserRole
from .service import FileService, get_FileService

router = APIRouter(prefix="/file", tags=["file"])


@router.post(
    "/upload",
    response_model=SuccessResult[dict],
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("File uploaded successfully", dict),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN(),
    },
)
@authorize(role=[UserRole.ADMIN])
async def upload_file(
    current_user: Annotated[User, Depends(get_current_user)],
    file: Annotated[UploadFile, File(...)],
    request: Request,
    bucket: str = Query("images", pattern="^(images|files)$"),
    file_service: FileService = Depends(get_FileService),
):
    """
    Upload a file directly through the API.

    Args:
        current_user (User): The current authenticated user.
        file (UploadFile): The uploaded file.
        bucket (str): Target bucket ("images" or "files").
        file_service (FileService): The file service dependency.
        request (Request): The HTTP request object.

    Returns:
        JSONResponse: Stored object metadata wrapped in a SuccessResult.
    """
    info = await file_service.upload_file(file, bucket)
    result = SuccessResult[dict](
        code=SuccessCodes.CREATED,
        message="File uploaded successfully",
        status_code=status.HTTP_201_CREATED,
        data=info,
    )
    return result.to_json_response(request)


@router.get("/object/{bucket}/{object_name:path}")
async def get_object(
    bucket: str,
    object_name: str,
    file_service: FileService = Depends(get_FileService),
):
    """
    Stream a stored object.

    Args:
        bucket (str): The bucket name.
        object_name (str): The object name.
        file_service (FileService): The file service dependency.

    Returns:
        StreamingResponse: The object bytes.
    """
    response, stat = await file_service.open_object(bucket, object_name)

    def stream():
        try:
            for chunk in response.stream(64 * 1024):
                yield chunk
        finally:
            response.close()
            response.release_conn()

    return StreamingResponse(
        stream(),
        media_type=stat.content_type or "application/octet-stream",
        headers={"Cache-Control": "public, max-age=31536000, immutable"},
    )


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
