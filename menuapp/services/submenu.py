import uuid

from fastapi import HTTPException, status, Depends

from menuapp.dao.models.submenu import Submenu
from menuapp.dao.schemas.submenu import (
    SubmenuCreate,
    SubmenuUpdate
)
from menuapp.dao.submenu import SubmenuDao, get_submenu_dao
from menuapp.exceptions.not_existent import ItemNotFound

__all__ = (
    'get_submenu_service',
    'SubmenuService',
)


class SubmenuService:
    """
    Submenu service
    """

    def __init__(self, dao: SubmenuDao):
        self.dao = dao

    async def get_all(self, menu_id: uuid.UUID) -> list[Submenu]:
        """ get all submenus """

        try:
            async with self.dao.session.begin():
                submenus = await self.dao.get_all(
                    menu_id=menu_id
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f"error message: {e}"
            )
        else:
            if not submenus:
                return []

            return submenus

    async def get_single_by_id(
            self,
            submenu_id: uuid.UUID
    ) -> Submenu:
        """ get single submenu by id """

        try:
            async with self.dao.session.begin():
                submenu = await self.dao.get_single_by_id(
                    submenu_id=submenu_id
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f"error message: {e}"
            )
        else:
            if not submenu:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="submenu not found"
                )

            return submenu

    async def create(
            self,
            menu_id: uuid.UUID,
            create_data: SubmenuCreate
    ) -> Submenu:
        """ insert new submenu """

        try:
            async with self.dao.session.begin():
                new_submenu = await self.dao.create(
                    menu_id=menu_id,
                    data=create_data
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f"error message: {e}"
            )
        else:
            return new_submenu

    async def update(
            self,
            submenu_id: uuid.UUID,
            update_data: SubmenuUpdate
    ) -> Submenu:
        """ update single submenu by id """

        try:
            async with self.dao.session.begin():
                updated_submenu = await self.dao.update(
                    submenu_id=submenu_id,
                    data=update_data
                )

                if not updated_submenu:
                    raise ItemNotFound(
                        f"submenu with: id {submenu_id} not found"
                    )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f"error message: {e}"
            )
        else:
            return updated_submenu

    async def delete(self, submenu_id: uuid.UUID):
        """ delete single submenu by id """

        try:
            async with self.dao.session.begin():
                is_deleted = await self.dao.delete(
                    submenu_id=submenu_id
                )

            if not is_deleted:
                raise ItemNotFound(
                    f"submenu with: id {submenu_id} not found"
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f"error message: {e}"
            )


async def get_submenu_service(
        dao: SubmenuDao = Depends(get_submenu_dao)
) -> SubmenuService:
    return SubmenuService(dao=dao)
