import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from menuapp.dao.models.dish import Dish
from menuapp.dao.schemas.dish import DishCreate, DishUpdate
from menuapp.dependencies import get_db

__all__ = (
    'DishDao',
    'get_dish_dao',
)


class DishDao:
    dish_model: Dish = Dish

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __get(self, dish_id: uuid.UUID) -> Dish:
        """ get dish scalar data """

        statement = select(
            self.dish_model
        ).where(self.dish_model.id == dish_id)

        result = await self.session.execute(
            statement=statement
        )
        dish: Dish = result.scalar_one_or_none()

        return dish

    async def get_all(self, submenu_id: uuid.UUID) -> list[Dish]:
        """ get all dishes """

        statement = select(
            self.dish_model.id,
            self.dish_model.title,
            self.dish_model.description,
            self.dish_model.price
        ).where(
            self.dish_model.submenu_id == submenu_id
        )

        result = await self.session.execute(
            statement=statement
        )
        dishes: list[Dish] = result.all()

        return dishes

    async def get_single_by_id(
            self,
            dish_id: uuid.UUID
    ) -> Dish | None:
        """ get single dish by id """

        statement = select(
            self.dish_model
        ).where(
            self.dish_model.id == dish_id
        )

        result = await self.session.execute(
            statement=statement
        )
        dish: Dish = result.one_or_none()

        return dish

    async def create(
            self,
            submenu_id: uuid.UUID,
            data: DishCreate
    ) -> Dish:
        """ insert new dish """

        new_dish = self.dish_model(
            **data.dict(),
            submenu_id=submenu_id
        )
        self.session.add(new_dish)

        return new_dish

    async def update(
            self,
            dish_id: uuid.UUID,
            data: DishUpdate
    ) -> Dish:
        """ update single dish by id """

        updated_dish = await self.__get(
            dish_id=dish_id
        )
        if updated_dish:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(updated_dish, key, value)
            self.session.add(updated_dish)

        return updated_dish

    async def delete(self, dish_id: uuid.UUID) -> bool:
        """ delete single dish by id """

        dish = await self.__get(
            dish_id=dish_id
        )

        if dish:
            await self.session.delete(dish)
            return True

        return False


async def get_dish_dao(
        session: AsyncSession = Depends(get_db)
) -> DishDao:
    return DishDao(session=session)
