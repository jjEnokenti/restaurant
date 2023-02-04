import uuid

from fastapi import APIRouter, Depends, status

from menu_app.services.menu import get_menu_service, MenuService
from menu_app.schemas import menu as m


menu_route = APIRouter()


@menu_route.get(
    "/menus",
    response_model=list[m.MenuRead],
    status_code=200
)
def get_all_menu(
        menu_service: MenuService = Depends(get_menu_service)
) -> list[m.MenuRead]:
    """
    list with menus or empty list
    """
    menus = menu_service.get_all()

    if not menus:
        return []

    return menus


@menu_route.get(
    "/menus/{menu_id}",
    response_model=m.MenuRead,
    status_code=status.HTTP_200_OK
)
def get_menu_by_id(
        menu_id: uuid.UUID,
        menu_service: MenuService = Depends(get_menu_service)
) -> m.MenuRead:
    """
    get single menu by id
    """

    return menu_service.get_single_by_id(menu_id)


@menu_route.post(
    "/menus",
    response_model=m.MenuRead,
    status_code=status.HTTP_201_CREATED
)
def create_menu(
        create_data: m.MenuCreate,
        menu_service: MenuService = Depends(get_menu_service)
) -> m.MenuRead:
    """
    create new menu
    """

    return menu_service.create(create_data)


@menu_route.patch(
    "/menus/{menu_id}",
    response_model=m.MenuRead,
    status_code=status.HTTP_200_OK
)
def update_menu_by_id(
        menu_id: uuid.UUID,
        update_data: m.MenuUpdate,
        menu_service: MenuService = Depends(get_menu_service)
) -> m.MenuRead:
    """
    update menu by id
    """

    return menu_service.update(menu_id, update_data)


@menu_route.delete(
    "/menus/{menu_id}",
    status_code=status.HTTP_200_OK
)
def delete_menu_by_id(
        menu_id: uuid.UUID,
        menu_service: MenuService = Depends(get_menu_service)
) -> str:
    """
    delete menu by id
    """
    menu_service.delete(menu_id)

    return f"menu {menu_id} was deleted"
