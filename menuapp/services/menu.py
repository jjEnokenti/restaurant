import uuid

from fastapi import HTTPException, status, Depends

from menuapp.dao.menu import MenuDao, get_menu_dao
from menuapp.dao.models.menu import Menu
from menuapp.dao.schemas.menu import MenuCreate, MenuUpdate
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

    async def get_all(self) -> list[Menu]:
        """ get all menus """

        try:
            async with self.dao.session.begin():
                menus = await self.dao.get_all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f'error message: {e}'
            )
        else:
            if not menus:
                return []

            return menus

    async def get_single_by_id(self, menu_id: uuid.UUID) -> Menu:
        """ get single menu by id """

        try:
            async with self.dao.session.begin():
                menu = await self.dao.get_single_by_id(
                    menu_id=menu_id
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f'error message: {e}'
            )
        else:
            if not menu:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='menu not found'
                )

            return menu

    async def create(self, create_data: MenuCreate) -> Menu:
        """ insert new menu """

        try:
            async with self.dao.session.begin():
                new_menu = await self.dao.create(
                    data=create_data
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f'error message: {e}'
            )
        else:
            return new_menu

    async def update(
            self,
            menu_id: uuid.UUID,
            update_data: MenuUpdate
    ) -> Menu:
        """ update single menu by id """

        try:
            async with self.dao.session.begin():
                updated_menu = await self.dao.update(
                    menu_id=menu_id,
                    data=update_data
                )

                if not updated_menu:
                    raise ItemNotFound(
                        f'menu with: id {menu_id} not found'
                    )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f'error message: {e}'
            )
        else:
            return updated_menu

    async def delete(self, menu_id: uuid.UUID):
        """ delete single menu by id """

        try:
            async with self.dao.session.begin():
                is_deleted = await self.dao.delete(menu_id=menu_id)

                if not is_deleted:
                    raise ItemNotFound(
                        f'menu with: id {menu_id} not found'
                    )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f'error message: {e}'
            )


async def get_menu_service(
        dao: MenuDao = Depends(get_menu_dao)
) -> MenuService:
    return MenuService(dao=dao)
