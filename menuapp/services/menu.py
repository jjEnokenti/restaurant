import uuid

from fastapi import HTTPException, status, Depends

from menuapp.dao.menu import MenuDao, get_menu_dao
from menuapp.dao.schemas.menu import MenuCreate, MenuUpdate, MenuRead
from menuapp.exceptions.not_existent import ItemNotFound

__all__ = (
    'get_menu_service',
    'MenuService',
)


class MenuService:
    """
    Menu service
    """

    def __init__(self, dao: MenuDao):
        self.dao = dao

    def get_all(self) -> list[MenuRead]:
        """ get all menus """

        try:
            with self.dao.session.begin():
                menus = self.dao.get_all()

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')
        else:
            return menus

    def get_single_by_id(self, menu_id: uuid.UUID) -> MenuRead:
        """ get single menu by id """

        try:
            with self.dao.session.begin():
                menu = self.dao.get_single_by_id(
                    menu_id=menu_id
                )

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')
        else:
            if not menu:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail='menu not found')

            return menu

    def create(self, create_data: MenuCreate) -> MenuCreate:
        """ insert new menu """

        try:
            with self.dao.session.begin():
                new_menu = self.dao.create(
                    data=create_data
                )

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')
        else:
            return new_menu

    def update(
            self,
            menu_id: uuid.UUID,
            update_data: MenuUpdate
    ) -> MenuUpdate:
        """ update single menu by id """

        try:
            with self.dao.session.begin():
                updated_menu = self.dao.update(
                    menu_id=menu_id,
                    data=update_data
                )

                if not updated_menu:
                    raise ItemNotFound(f'menu with: id {menu_id} not found')

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')
        else:
            return updated_menu

    def delete(self, menu_id):
        """ delete single menu by id """

        try:
            with self.dao.session.begin():
                is_deleted = self.dao.delete(menu_id=menu_id)
                if not is_deleted:
                    raise ItemNotFound(f'menu with: id {menu_id} not found')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')


def get_menu_service(
        dao: MenuDao = Depends(get_menu_dao)
) -> MenuService:
    return MenuService(dao=dao)
