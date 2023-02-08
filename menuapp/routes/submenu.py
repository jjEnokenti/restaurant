import uuid

from fastapi import APIRouter, Depends, status

from menuapp.dao.schemas import submenu as s
from menuapp.services.submenu import get_submenu_service, SubmenuService

submenu_route = APIRouter()


@submenu_route.get(
    '/submenus',
    response_model=list[s.SubmenuRead],
    summary='get submenus',
    description='returns response all submenus or empty list',
    status_code=status.HTTP_200_OK
)
def get_all_submenus(
        menu_id: uuid.UUID,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> list[s.SubmenuRead]:
    submenus = submenu_service.get_all(menu_id=menu_id)

    if not submenus:
        return []

    return submenus


@submenu_route.get(
    '/submenus/{submenu_id}',
    response_model=s.SubmenuRead,
    summary='get single submenu by id',
    description='returns detailed response a submenu by id',
    status_code=status.HTTP_200_OK
)
def get_single_submenu_by_id(
        submenu_id: uuid.UUID,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> s.SubmenuRead:
    return submenu_service.get_single_by_id(submenu_id=submenu_id)


@submenu_route.post(
    '/submenus',
    response_model=s.SubmenuRead,
    summary='create new submenu',
    description='creates a menu, return detailed response with a new submenu',
    status_code=status.HTTP_201_CREATED
)
def create_submenu(
        menu_id: uuid.UUID,
        create_data: s.SubmenuCreate,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> s.SubmenuCreate:
    return submenu_service.create(
        menu_id=menu_id,
        create_data=create_data
    )


@submenu_route.patch(
    '/submenus/{submenu_id}',
    response_model=s.SubmenuRead,
    summary='update submenu by id',
    description='updates menu by id, returns detailed response with updated submenu',
    status_code=status.HTTP_200_OK
)
def update_submenu_by_id(
        submenu_id: uuid.UUID,
        update_data: s.SubmenuUpdate,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> s.SubmenuUpdate:
    return submenu_service.update(
        submenu_id=submenu_id,
        update_data=update_data
    )


@submenu_route.delete(
    "/submenus/{submenu_id}",
    summary='delete submenu by id',
    description='delete submenu by id, return status response information',
    status_code=status.HTTP_200_OK
)
def delete_submenu_by_id(
        submenu_id: uuid.UUID,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> str:
    submenu_service.delete(submenu_id=submenu_id)

    return f"submenu {submenu_id} was deleted"
