import uuid

from fastapi import APIRouter, Depends, status

from app.dao.schemas.menu import (
    MenuCreate,
    MenuUpdate,
    MenuRead
)
from app.services.menu import get_menu_service, MenuService

menu_route = APIRouter()


@menu_route.get(
    '/menus/',
    response_model=list[MenuRead],
    summary='get menus',
    description='returns response all menus or empty list',
    status_code=200
)
async def get_all_menu(
        menu_service: MenuService = Depends(get_menu_service)
) -> list[MenuRead]:
    return await menu_service.get_all()


@menu_route.get(
    '/menus/{menu_id}/',
    response_model=MenuRead,
    summary='get single menu by id',
    description='returns detailed response a menu by id',
    status_code=status.HTTP_200_OK
)
async def get_menu_by_id(
        menu_id: uuid.UUID,
        menu_service: MenuService = Depends(get_menu_service)
) -> MenuRead:
    return await menu_service.get_single_by_id(menu_id)


@menu_route.post(
    '/menus/',
    response_model=MenuRead,
    summary='create new menu',
    description='return detailed response with a new menu',
    status_code=status.HTTP_201_CREATED
)
async def create_menu(
        create_data: MenuCreate,
        menu_service: MenuService = Depends(get_menu_service)
) -> MenuRead:
    return await menu_service.create(
        create_data=create_data
    )


@menu_route.patch(
    '/menus/{menu_id}/',
    response_model=MenuRead,
    summary='update menu by id',
    description='returns detailed response with updated menu',
    status_code=status.HTTP_200_OK
)
async def update_menu_by_id(
        menu_id: uuid.UUID,
        update_data: MenuUpdate,
        menu_service: MenuService = Depends(get_menu_service)
) -> MenuRead:
    return await menu_service.update(
        menu_id=menu_id,
        update_data=update_data
    )


@menu_route.delete(
    '/menus/{menu_id}/',
    summary='delete menu by id',
    description='delete menu by id, return status response information',
    status_code=status.HTTP_200_OK
)
async def delete_menu_by_id(
        menu_id: uuid.UUID,
        menu_service: MenuService = Depends(get_menu_service)
) -> str:
    await menu_service.delete(menu_id)

    return f'menu {menu_id} was deleted'
