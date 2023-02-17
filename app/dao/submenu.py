import uuid

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.models.dish import Dish
from app.dao.models.submenu import Submenu
from app.dao.schemas.submenu import SubmenuCreate, SubmenuUpdate
from app.dependencies import get_db

__all__ = (
    'get_submenu_dao',
    'SubmenuDao',
)


class SubmenuDao:
    submenu_model: Submenu = Submenu
    dish_model: Dish = Dish

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __get(self, submenu_id: uuid.UUID) -> Submenu:
        """ get submenu scalar data """

        statement = select(
            self.submenu_model
        ).where(self.submenu_model.id == submenu_id)

        result = await self.session.execute(
            statement=statement
        )
        submenu: Submenu = result.scalar_one_or_none()

        return submenu

    async def get_all(self, menu_id: uuid.UUID) -> list[Submenu]:
        """ get all submenus """

        statement = select(
            self.submenu_model.id,
            self.submenu_model.title,
            self.submenu_model.description,
            func.count(self.dish_model.id).label("dishes_count")
        ).group_by(
            self.submenu_model.id
        ).outerjoin(
            self.dish_model,
            self.dish_model.submenu_id == self.submenu_model.id
        ).where(
            self.submenu_model.menu_id == menu_id
        )

        result = await self.session.execute(
            statement=statement
        )
        submenus: list[Submenu] = result.all()

        return submenus

    async def get_single_by_id(
            self,
            submenu_id: uuid.UUID
    ) -> Submenu | None:
        """ get single submenu by id """

        statement = select(
            self.submenu_model.id,
            self.submenu_model.title,
            self.submenu_model.description,
            func.count(self.dish_model.id).label("dishes_count")
        ).group_by(
            self.submenu_model.id
        ).outerjoin(
            self.dish_model,
            self.dish_model.submenu_id == self.submenu_model.id
        ).where(
            self.submenu_model.id == submenu_id
        )

        result = await self.session.execute(
            statement=statement
        )
        submenu: Submenu = result.one_or_none()

        return submenu

    async def create(
            self,
            menu_id: uuid.UUID,
            data: SubmenuCreate
    ) -> Submenu:
        """ insert new submenu """

        new_submenu = self.submenu_model(
            **data.dict(),
            menu_id=menu_id
        )
        self.session.add(new_submenu)

        return new_submenu

    async def update(
            self,
            submenu_id: uuid.UUID,
            data: SubmenuUpdate
    ) -> Submenu:
        """ update single submenu by id """

        updated_submenu = await self.__get(
            submenu_id=submenu_id
        )
        if updated_submenu:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(updated_submenu, key, value)
            self.session.add(updated_submenu)

        return updated_submenu

    async def delete(self, submenu_id: uuid.UUID) -> bool:
        """ delete single submenu by id from db """

        submenu = await self.__get(
            submenu_id=submenu_id
        )

        if submenu:
            await self.session.delete(submenu)
            return True

        return False


async def get_submenu_dao(
        session: AsyncSession = Depends(get_db)
) -> SubmenuDao:
    return SubmenuDao(session=session)
