import uuid

from fastapi import Depends
from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.models.dish import Dish
from app.dao.models.menu import Menu
from app.dao.models.submenu import Submenu
from app.dao.schemas.menu import MenuCreate, MenuUpdate
from app.dependencies import get_db

__all__ = (
    'get_menu_dao',
    'MenuDao',
)


class MenuDao:
    menu_model: Menu = Menu
    submenu_model: Submenu = Submenu
    dish_model: Dish = Dish

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __get(self, menu_id: uuid.UUID) -> Menu:
        """ get menu scalar data """

        statement = select(
            self.menu_model
        ).where(self.menu_model.id == menu_id)

        result = await self.session.execute(
            statement=statement
        )
        menu: Menu = result.scalar_one_or_none()

        return menu

    async def get_all(self) -> list[Menu]:
        """ get all menus """

        statement = select(
            self.menu_model.id,
            self.menu_model.title,
            self.menu_model.description,
            func.count(distinct(
                self.submenu_model.id)
            ).label('submenus_count'),
            func.count(self.dish_model.id).label('dishes_count')
        ).outerjoin(
            self.submenu_model,
            self.menu_model.id == self.submenu_model.menu_id
        ).outerjoin(
            self.dish_model,
            self.submenu_model.id == self.dish_model.submenu_id
        ).group_by(
            self.menu_model.id
        )

        result = await self.session.execute(
            statement=statement
        )
        menus: list[Menu] = result.all()

        return menus

    async def get_single_by_id(self, menu_id: uuid.UUID) -> Menu:
        """ get single menu by id """

        statement = select(
            self.menu_model.id,
            self.menu_model.title,
            self.menu_model.description,
            func.count(distinct(
                self.submenu_model.id)
            ).label('submenus_count'),
            func.count(self.dish_model.id).label('dishes_count')
        ).outerjoin(
            self.submenu_model,
            self.menu_model.id == self.submenu_model.menu_id
        ).outerjoin(
            self.dish_model,
            self.submenu_model.id == self.dish_model.submenu_id
        ).group_by(
            self.menu_model.id
        ).where(self.menu_model.id == menu_id)

        result = await self.session.execute(
            statement=statement
        )
        menu: Menu = result.one_or_none()

        return menu

    async def create(self, data: MenuCreate) -> Menu:
        """ insert new menu """

        new_menu = self.menu_model(**data.dict())
        self.session.add(new_menu)

        return new_menu

    async def update(
            self,
            menu_id: uuid.UUID,
            data: MenuUpdate
    ) -> Menu | None:
        """ update single menu by id """

        updated_menu = await self.__get(menu_id=menu_id)
        if updated_menu:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(updated_menu, key, value)
            self.session.add(updated_menu)

        return updated_menu

    async def delete(self, menu_id: uuid.UUID) -> bool:
        """ delete single menu by id """
        menu = await self.__get(menu_id=menu_id)

        if menu:
            await self.session.delete(menu)
            return True

        return False


async def get_menu_dao(
        session: AsyncSession = Depends(get_db)
) -> MenuDao:
    return MenuDao(session=session)
