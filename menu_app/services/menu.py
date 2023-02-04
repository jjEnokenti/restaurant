import uuid

from fastapi import HTTPException, status, Depends

from menu_app.dao.menu import MenuDao, get_menu_dao
from menu_app.dao.schemas.menu import MenuCreate, MenuUpdate, MenuRead
from menu_app.exceptions.not_existent import ItemNotFound

__all__ = (
    'get_menu_service',
    'MenuService',
)


class MenuService:
    """
    Menu service
    """

    def __init__(self, session: MenuDao):
        self.session = session

    def get_all(self) -> list[MenuRead]:
        """
        get all menus from db
        """
        try:
            with self.session.session.begin():
                menus = self.session.get_all()

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')
        else:
            return menus

    def get_single_by_id(self, menu_id: uuid.UUID) -> MenuRead:
        """
        get single menu by id from db
        """
        try:
            with self.session.session.begin():
                menu = self.session.get_single_by_id(menu_id=menu_id)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')
        else:
            if not menu:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail='menu not found')

            return menu

    def create(self, create_data: MenuCreate):
        """
        insert new menu into db
        """
        try:
            with self.session.session.begin():
                new_menu = self.session.create(data=create_data)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')
        else:
            return new_menu

    def update(
            self,
            menu_id: uuid.UUID,
            update_data: MenuUpdate
    ):
        """
        update single menu by id into db
        """
        try:
            with self.session.session.begin():
                updated_menu = self.session.update(menu_id=menu_id, data=update_data)

                if not updated_menu:
                    raise ItemNotFound(f'menu with: id {menu_id} not found')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')
        else:
            return updated_menu

    def delete(self, menu_id):
        """
        delete single menu by id from db
        """
        try:
            with self.session.session.begin():
                is_deleted = self.session.delete(menu_id=menu_id)
                if not is_deleted:
                    raise ItemNotFound(f'menu with: id {menu_id} not found')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')


def get_menu_service(
        dao: MenuDao = Depends(get_menu_dao)
) -> MenuService:
    return MenuService(session=dao)
