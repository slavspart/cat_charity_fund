from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_before_edit,
    check_invested,
    check_name_duplicate,
    check_object_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)

router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    # schema instance
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    await check_name_duplicate(
        charity_project.name, CharityProject, charity_project_crud, session
    )
    new_project = await charity_project_crud.create(charity_project, session)
    await charity_project_crud.invest_donation(new_project, session)
    # getting free money from donations to the project
    return new_project


@router.get(
    "/",
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    "/{charity_project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_object_exists(
        charity_project_id, charity_project_crud, session
    )
    check_before_edit(project, obj_in)
    # check project is not closed and full amount is more than invested

    if obj_in.name is not None and obj_in.name != project.name:
        await check_name_duplicate(
            obj_in.name, CharityProject, charity_project_crud, session
        )

    project = await charity_project_crud.update(project, obj_in, session)
    return project


@router.delete(
    "/{charity_project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    charity_project = await check_object_exists(
        charity_project_id, charity_project_crud, session
    )
    check_invested(charity_project)
    charity_project = await charity_project_crud.remove(charity_project, session)
    return charity_project
