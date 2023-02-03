import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import menu_app.services.submenu as submenu_service
from menu_app.dependences import get_db
from menu_app.schemas import submenu as s

submenu_route = APIRouter()


@submenu_route.get(
    "/submenus",
    response_model=list[s.SubmenuRead],
    status_code=status.HTTP_200_OK
)
def get_all_submenus(
        menu_id: uuid.UUID,
        db: Session = Depends(get_db)
) -> list[s.SubmenuRead]:
    """
    get all submenus
    """
    submenus = submenu_service.get_all(db, menu_id)
    if not submenus:
        return []

    return submenus


@submenu_route.get(
    "/submenus/{submenu_id}",
    response_model=s.SubmenuRead,
    status_code=status.HTTP_200_OK
)
def get_single_submenu_by_id(
        submenu_id: uuid.UUID,
        db: Session = Depends(get_db)
) -> s.SubmenuRead:
    """
    get single submenu by id
    """

    return submenu_service.get_single_by_id(db, submenu_id)


@submenu_route.post(
    "/submenus",
    response_model=s.SubmenuRead,
    status_code=status.HTTP_201_CREATED
)
def create_submenu(
        menu_id: uuid.UUID,
        create_data: s.SubmenuCreate,
        db: Session = Depends(get_db)
) -> s.SubmenuRead:
    """
    create submenu
    """

    return submenu_service.create(db, menu_id, create_data)


@submenu_route.patch(
    "/submenus/{submenu_id}",
    response_model=s.SubmenuRead,
    status_code=status.HTTP_200_OK
)
def update_submenu_by_id(
        submenu_id: uuid.UUID,
        update_data: s.SubmenuUpdate,
        db: Session = Depends(get_db)
) -> s.SubmenuRead:
    """
    update submenu by id
    """

    return submenu_service.update(db, submenu_id, update_data)


@submenu_route.delete(
    "/submenus/{submenu_id}",
    status_code=status.HTTP_200_OK
)
def delete_submenu_by_id(
        submenu_id: uuid.UUID,
        db: Session = Depends(get_db)
) -> str:
    """
    delete submenu by id
    """
    submenu_service.delete(db, submenu_id)

    return f"submenu {submenu_id} was deleted"
