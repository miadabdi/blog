"""
API router for Project endpoints.
Handles HTTP requests for project CRUD operations.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request, status

from ..auth.auth import authorize, get_current_active_user
from ..auth.models import User
from ..common.deps import AsyncSessionDep
from ..common.http_responses.doc_responses import (
    ResponseErrorDoc,
    ResponseSuccessDoc,
)
from ..common.http_responses.success_response import SuccessCodes
from ..common.http_responses.success_result import SuccessResult
from ..common.user_role import UserRole
from .schemas import CreateProject, ProjectPublic, UpdateProject
from .service import ProjectService, get_ProjectService

router = APIRouter(prefix="/project", tags=["project"])

ProjectServiceDep = Annotated[ProjectService, Depends(get_ProjectService)]


@router.post(
    "/",
    response_model=SuccessResult[ProjectPublic],
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("Project created successfully", ProjectPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_409_CONFLICT(),
    },
)
@authorize(role=[UserRole.ADMIN])
async def create_project(
    project: Annotated[CreateProject, Body()],
    session: AsyncSessionDep,
    service: ProjectServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    """
    Create a new project.
    """
    created_project = await service.create_project(project, current_user, session)
    public_project = ProjectPublic.model_validate(created_project)
    result = SuccessResult[ProjectPublic](
        code=SuccessCodes.CREATED,
        message="Project created successfully",
        status_code=status.HTTP_201_CREATED,
        data=public_project,
    )
    return result.to_json_response(request)


@router.get(
    "/",
    response_model=SuccessResult[list[ProjectPublic]],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Projects fetched successfully", list[ProjectPublic]),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
    },
)
async def get_all_projects(
    session: AsyncSessionDep, service: ProjectServiceDep, request: Request
):
    """
    Retrieve all projects, newest first.
    """
    projects = await service.get_all_projects(session)
    public_projects = [ProjectPublic.model_validate(project) for project in projects]
    result = SuccessResult[list[ProjectPublic]](
        code=SuccessCodes.SUCCESS,
        message="Projects fetched successfully",
        status_code=status.HTTP_200_OK,
        data=public_projects,
    )
    return result.to_json_response(request)


@router.get(
    "/slug/{slug}",
    response_model=SuccessResult[ProjectPublic],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Project fetched successfully", ProjectPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
    },
)
async def get_project_by_slug(
    slug: str, session: AsyncSessionDep, service: ProjectServiceDep, request: Request
):
    """
    Retrieve a project by its slug.
    """
    project = await service.get_project_by_slug(slug, session)
    public_project = ProjectPublic.model_validate(project)
    result = SuccessResult[ProjectPublic](
        code=SuccessCodes.SUCCESS,
        message="Project fetched successfully",
        status_code=status.HTTP_200_OK,
        data=public_project,
    )
    return result.to_json_response(request)


@router.patch(
    "/{project_id}",
    response_model=SuccessResult[ProjectPublic],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Project updated successfully", ProjectPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_409_CONFLICT(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN(),
    },
)
@authorize(role=[UserRole.ADMIN])
async def update_project(
    project_id: int,
    project: Annotated[UpdateProject, Body()],
    session: AsyncSessionDep,
    service: ProjectServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    """
    Update an existing project.
    """
    updated_project = await service.update_project(project_id, project, session)
    public_project = ProjectPublic.model_validate(updated_project)
    result = SuccessResult[ProjectPublic](
        code=SuccessCodes.SUCCESS,
        message="Project updated successfully",
        status_code=status.HTTP_200_OK,
        data=public_project,
    )
    return result.to_json_response(request)


@router.get(
    "/{project_id}",
    response_model=SuccessResult[ProjectPublic],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Project fetched successfully", ProjectPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
    },
)
async def get_project_by_id(
    project_id: int, session: AsyncSessionDep, service: ProjectServiceDep, request: Request
):
    """
    Retrieve a project by its ID.
    """
    project = await service.get_project_by_id(project_id, session)
    public_project = ProjectPublic.model_validate(project)
    result = SuccessResult[ProjectPublic](
        code=SuccessCodes.SUCCESS,
        message="Project fetched successfully",
        status_code=status.HTTP_200_OK,
        data=public_project,
    )
    return result.to_json_response(request)


@router.delete(
    "/{project_id}",
    response_model=SuccessResult[ProjectPublic],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Project deleted successfully", ProjectPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN(),
    },
)
@authorize(role=[UserRole.ADMIN])
async def delete_project(
    project_id: int,
    session: AsyncSessionDep,
    service: ProjectServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    """
    Delete a project by its ID.
    """
    deleted_project = await service.delete_project(project_id, session)
    public_project = ProjectPublic.model_validate(deleted_project)
    result = SuccessResult[ProjectPublic](
        code=SuccessCodes.SUCCESS,
        message="Project deleted successfully",
        status_code=status.HTTP_200_OK,
        data=public_project,
    )
    return result.to_json_response(request)
