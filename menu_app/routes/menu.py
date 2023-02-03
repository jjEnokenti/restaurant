import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import menu_app.services.menu as menu_service
from menu_app.dependences import get_db
from menu_app.schemas import menu as m


menu_route = APIRouter()


@menu_route.get(
    "/menus",
    response_model=list[m.MenuRead],
    status_code=200
)
def get_all_menu(
        db: Session = Depends(get_db)
) -> list[m.MenuRead]:
    """
    get all menus
    """
    menus = menu_service.get_all(db)

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
        db: Session = Depends(get_db)
) -> m.MenuRead:
    """
    get single menu by id
    """

    return menu_service.get_single_by_id(db, menu_id)


@menu_route.post(
    "/menus",
    response_model=m.MenuRead,
    status_code=status.HTTP_201_CREATED
)
def create_menu(
        create_data: m.MenuCreate,
        db: Session = Depends(get_db)
) -> m.MenuRead:
    """
    create new menu
    """

    return menu_service.create(db, create_data)


@menu_route.patch(
    "/menus/{menu_id}",
    response_model=m.MenuRead,
    status_code=status.HTTP_200_OK
)
def update_menu_by_id(
        menu_id: uuid.UUID,
        update_data: m.MenuUpdate,
        db: Session = Depends(get_db)
) -> m.MenuRead:
    """
    update menu by id
    """

    return menu_service.update(db, menu_id, update_data)


@menu_route.delete(
    "/menus/{menu_id}",
    status_code=status.HTTP_200_OK
)
def delete_menu_by_id(
        menu_id: uuid.UUID,
        db: Session = Depends(get_db)
) -> str:
    """
    delete menu by id
    """
    menu_service.delete(db, menu_id)

    return f"menu {menu_id} was deleted"
