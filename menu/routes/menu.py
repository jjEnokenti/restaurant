import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import menu.services.menu as menu_service
from menu.dependences import get_db
from menu.schemas import MenuCreate, MenuRead, MenuUpdate


menu_route = APIRouter()


@menu_route.get("/menus", response_model=list[MenuRead], status_code=200)
def get_all_menu(db: Session = Depends(get_db)):
    """
    get all menus
    """
    menus = menu_service.get_all(db)

    if not menus:
        return []

    # set value to dishes_count and submenus_count
    for menu in menus:
        menu.dishes_count = 0
        menu.submenus_count = len(menu.submenu)
        for submenu in menu.submenu:
            menu.dishes_count += len(submenu.dish)

    return menus


@menu_route.get("/menus/{menu_id}", response_model=MenuRead, status_code=200)
def get_menu_by_id(menu_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    get single menu by id
    """
    menu = menu_service.get_single_by_id(db, menu_id)

    # set value to dishes_count and submenus_count
    menu.submenus_count = len(menu.submenu)
    menu.dishes_count = 0
    for submenu in menu.submenu:
        menu.dishes_count += len(submenu.dish)

    return menu


@menu_route.post("/menus", response_model=MenuRead, status_code=201)
def create_menu(create_data: MenuCreate, db: Session = Depends(get_db)):
    """
    create new menu
    """
    new_menu = menu_service.create(db, create_data)

    return new_menu


@menu_route.patch("/menus/{menu_id}", response_model=MenuRead, status_code=200)
def update_menu_by_id(menu_id: uuid.UUID, update_data: MenuUpdate, db: Session = Depends(get_db)):
    """
    update menu by id
    """
    updated_menu = menu_service.update(db, menu_id, update_data)

    return updated_menu


@menu_route.delete("/menus/{menu_id}", status_code=200)
def delete_menu_by_id(menu_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    delete menu by id
    """
    menu_service.delete(db, menu_id)

    return f"menu {menu_id} was deleted"
