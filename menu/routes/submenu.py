import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import menu.services.submenu as submenu_service
from menu.dependences import get_db
from menu.schemas import SubmenuCreate, SubmenuRead, SubmenuUpdate


submenu_route = APIRouter()


@submenu_route.get("/submenus", response_model=list[SubmenuRead], status_code=200)
def get_all_submenus(menu_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    get all submenus
    """
    submenus = submenu_service.get_all(db, menu_id)
    if not submenus:
        return []

    return submenus


@submenu_route.get("/submenus/{submenu_id}", response_model=SubmenuRead, status_code=200)
def get_single_submenu_by_id(submenu_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    get single submenu by id
    """
    submenu = submenu_service.get_single_by_id(db, submenu_id)

    return submenu


@submenu_route.post("/submenus", response_model=SubmenuRead, status_code=201)
def create_submenu(menu_id: uuid.UUID, create_data: SubmenuCreate, db: Session = Depends(get_db)):
    """
    create submenu
    """
    new_submenu = submenu_service.create(db, menu_id, create_data)

    return new_submenu


@submenu_route.patch("/submenus/{submenu_id}", response_model=SubmenuRead, status_code=200)
def update_submenu_by_id(submenu_id: uuid.UUID, update_data: SubmenuUpdate, db: Session = Depends(get_db)):
    """
    update submenu by id
    """
    updated_submenu = submenu_service.update(db, submenu_id, update_data)

    return updated_submenu


@submenu_route.delete("/submenus/{submenu_id}", status_code=200)
def delete_submenu_by_id(submenu_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    delete submenu by id
    """
    submenu_service.delete(db, submenu_id)

    return f"submenu {submenu_id} was deleted"
