import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.engine import row
from sqlalchemy.orm import Session

from menuapp.dao.models import dish as d
from menuapp.dao.schemas.dish import DishCreate, DishUpdate
from menuapp.dependences import get_db

__all__ = (
    'DishDao',
    'get_dish_dao',
)


class DishDao:
    dish_model: d.Dish = d.Dish

    def __init__(self, session: Session):
        self.session = session

    def __get(self, dish_id: uuid.UUID) -> dish_model:
        """ get dish scalar data """

        statement = select(
            self.dish_model
        ).where(self.dish_model.id == dish_id)

        dish = self.session.execute(
            statement=statement
        ).scalar_one_or_none()

        return dish

    def get_all(self, submenu_id: uuid.UUID) -> list[row]:
        """ get all dishes """

        statement = select(
            self.dish_model
        ).where(
            self.dish_model.submenu_id == submenu_id
        )

        dishes = self.session.execute(
            statement=statement
        ).all()

        return dishes

    def get_single_by_id(self, dish_id: uuid.UUID) -> row or None:
        """ get single dish by id """

        statement = select(
            self.dish_model
        ).where(
            self.dish_model.id == dish_id
        )

        dish = self.session.execute(
            statement=statement
        ).one_or_none()

        return dish

    def create(
            self,
            submenu_id: uuid.UUID,
            data: DishCreate
    ) -> DishCreate:
        """ insert new dish """

        new_dish = self.dish_model(
            **data.dict(),
            submenu_id=submenu_id
        )
        self.session.add(new_dish)

        return new_dish

    def update(
            self,
            dish_id: uuid.UUID,
            data: DishUpdate
    ) -> DishUpdate:
        """ update single dish by id """

        updated_dish = self.__get(
            dish_id=dish_id
        )
        if dish_id:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(updated_dish, key, value)
            self.session.add(updated_dish)

        return updated_dish

    def delete(self, dish_id: uuid.UUID):
        """ delete single dish by id """

        dish = self.__get(
            dish_id=dish_id
        )

        if dish:
            self.session.delete(dish)
            return True

        return False


def get_dish_dao(
        session: Session = Depends(get_db)
) -> DishDao:
    return DishDao(session=session)
