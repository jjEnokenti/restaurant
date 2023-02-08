import uuid

from fastapi import HTTPException, status, Depends

from menuapp.dao.submenu import SubmenuDao, get_submenu_dao
from menuapp.dao.schemas.submenu import SubmenuRead, SubmenuCreate, SubmenuUpdate
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

    def get_all(self, menu_id: uuid.UUID) -> list[SubmenuRead]:
        """ get all submenus """

        try:
            with self.dao.session.begin():
                submenus = self.dao.get_all(
                    menu_id=menu_id
                )

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f"error message: {e}")
        else:
            return submenus

    def get_single_by_id(self, submenu_id: uuid.UUID) -> SubmenuRead:
        """ get single submenu by id """

        try:
            with self.dao.session.begin():
                submenu = self.dao.get_single_by_id(
                    submenu_id=submenu_id
                )

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f"error message: {e}")
        else:
            if not submenu:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="submenu not found")

            return submenu

    def create(
            self,
            menu_id: uuid.UUID,
            create_data: SubmenuCreate
    ) -> SubmenuCreate:
        """ insert new submenu """

        try:
            with self.dao.session.begin():
                new_submenu = self.dao.create(
                    menu_id=menu_id,
                    data=create_data
                )

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f"error message: {e}")
        else:
            return new_submenu

    def update(
            self,
            submenu_id: uuid.UUID,
            update_data: SubmenuUpdate
    ) -> SubmenuUpdate:
        """ update single submenu by id """

        try:
            with self.dao.session.begin():
                updated_submenu = self.dao.update(
                    submenu_id=submenu_id,
                    data=update_data
                )

                if not updated_submenu:
                    raise ItemNotFound(f"submenu with: id {submenu_id} not found")

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f"error message: {e}")
        else:
            return updated_submenu

    def delete(self, submenu_id: uuid.UUID):
        """ delete single submenu by id """

        try:
            with self.dao.session.begin():
                is_deleted = self.dao.delete(
                    submenu_id=submenu_id
                )

            if not is_deleted:
                raise ItemNotFound(f"submenu with: id {submenu_id} not found")

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f"error message: {e}")


def get_submenu_service(
        dao: SubmenuDao = Depends(get_submenu_dao)
) -> SubmenuService:
    return SubmenuService(dao=dao)
