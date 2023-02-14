import uuid

from fastapi import APIRouter, Depends, status

from menuapp.dao.schemas.submenu import (
    SubmenuRead,
    SubmenuCreate,
    SubmenuUpdate
)
from menuapp.services.submenu import get_submenu_service, SubmenuService

submenu_route = APIRouter()


@submenu_route.get(
    '/submenus/',
    response_model=list[SubmenuRead],
    summary='get submenus',
    description='returns response all submenus or empty list',
    status_code=status.HTTP_200_OK
)
async def get_all_submenus(
        menu_id: uuid.UUID,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> list[SubmenuRead]:
    return await submenu_service.get_all(menu_id=menu_id)


@submenu_route.get(
    '/submenus/{submenu_id}/',
    response_model=SubmenuRead,
    summary='get single submenu by id',
    description='returns detailed response a submenu by id',
    status_code=status.HTTP_200_OK
)
async def get_single_submenu_by_id(
        submenu_id: uuid.UUID,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> SubmenuRead:
    return await submenu_service.get_single_by_id(
        submenu_id=submenu_id
    )


@submenu_route.post(
    '/submenus/',
    response_model=SubmenuRead,
    summary='create new submenu',
    description='return detailed response with a new submenu',
    status_code=status.HTTP_201_CREATED
)
async def create_submenu(
        menu_id: uuid.UUID,
        create_data: SubmenuCreate,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> SubmenuRead:
    return await submenu_service.create(
        menu_id=menu_id,
        create_data=create_data
    )


@submenu_route.patch(
    '/submenus/{submenu_id}/',
    response_model=SubmenuRead,
    summary='update submenu by id',
    description='returns detailed response with updated submenu',
    status_code=status.HTTP_200_OK
)
async def update_submenu_by_id(
        submenu_id: uuid.UUID,
        update_data: SubmenuUpdate,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> SubmenuUpdate:
    return await submenu_service.update(
        submenu_id=submenu_id,
        update_data=update_data
    )


@submenu_route.delete(
    "/submenus/{submenu_id}/",
    summary='delete submenu by id',
    description='delete submenu by id, return status response information',
    status_code=status.HTTP_200_OK
)
async def delete_submenu_by_id(
        submenu_id: uuid.UUID,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> str:
    await submenu_service.delete(submenu_id=submenu_id)

    return f"submenu {submenu_id} was deleted"
