import uuid

from fastapi import APIRouter, Depends, status

from menuapp.dao.schemas import menu as m
from menuapp.services.menu import get_menu_service, MenuService

menu_route = APIRouter()


@menu_route.get(
    '/menus',
    response_model=list[m.MenuRead],
    summary='get menus',
    description='returns response all menus or empty list',
    status_code=200
)
def get_all_menu(
        menu_service: MenuService = Depends(get_menu_service)
) -> list[m.MenuRead]:
    menus = menu_service.get_all()

    if not menus:
        return []

    return menus


@menu_route.get(
    '/menus/{menu_id}',
    response_model=m.MenuRead,
    summary='get single menu by id',
    description='returns detailed response a menu by id',
    status_code=status.HTTP_200_OK
)
def get_menu_by_id(
        menu_id: uuid.UUID,
        menu_service: MenuService = Depends(get_menu_service)
) -> m.MenuRead:
    return menu_service.get_single_by_id(menu_id)


@menu_route.post(
    '/menus',
    response_model=m.MenuRead,
    summary='create new menu',
    description='creates a menu, return detailed response with a new menu',
    status_code=status.HTTP_201_CREATED
)
def create_menu(
        create_data: m.MenuCreate,
        menu_service: MenuService = Depends(get_menu_service)
) -> m.MenuCreate:
    return menu_service.create(
        create_data=create_data
    )


@menu_route.patch(
    '/menus/{menu_id}',
    response_model=m.MenuRead,
    summary='update menu by id',
    description='updates menu by id, returns detailed response with updated menu',
    status_code=status.HTTP_200_OK
)
def update_menu_by_id(
        menu_id: uuid.UUID,
        update_data: m.MenuUpdate,
        menu_service: MenuService = Depends(get_menu_service)
) -> m.MenuUpdate:
    return menu_service.update(menu_id, update_data)


@menu_route.delete(
    '/menus/{menu_id}',
    summary='delete menu by id',
    description='delete menu by id, return status response information',
    status_code=status.HTTP_200_OK
)
def delete_menu_by_id(
        menu_id: uuid.UUID,
        menu_service: MenuService = Depends(get_menu_service)
) -> str:
    menu_service.delete(menu_id)

    return f'menu {menu_id} was deleted'
