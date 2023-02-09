import uuid

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.engine import row
from sqlalchemy.orm import Session

from menuapp.dao.models import dish as d, submenu as s
from menuapp.dao.schemas.submenu import SubmenuCreate, SubmenuUpdate
from menuapp.dependences import get_db

__all__ = (
    'get_submenu_dao',
    'SubmenuDao',
)


class SubmenuDao:
    submenu_model: s.Submenu = s.Submenu
    dish_model: d.Dish = d.Dish

    def __init__(self, session: Session):
        self.session = session

    def __get(self, submenu_id: uuid.UUID) -> submenu_model:
        """ get submenu scalar data """

        statement = select(
            self.submenu_model
        ).where(self.submenu_model.id == submenu_id)

        return self.session.execute(
            statement=statement
        ).scalar_one_or_none()

    def get_all(self, menu_id: uuid.UUID) -> list[row]:
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

        return self.session.execute(
            statement=statement
        ).all()

    def get_single_by_id(self, submenu_id: uuid.UUID) -> row or None:
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

        return self.session.execute(
            statement=statement
        ).one_or_none()

    def create(
            self,
            menu_id: uuid.UUID,
            data: SubmenuCreate
    ) -> SubmenuCreate:
        """ insert new submenu """

        new_submenu = self.submenu_model(
            **data.dict(),
            menu_id=menu_id
        )
        self.session.add(new_submenu)

        return new_submenu

    def update(
            self,
            submenu_id: uuid.UUID,
            data: SubmenuUpdate
    ) -> SubmenuUpdate:
        """ update single submenu by id """

        updated_submenu = self.__get(
            submenu_id=submenu_id
        )
        if updated_submenu:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(updated_submenu, key, value)
            self.session.add(updated_submenu)

        return updated_submenu

    def delete(self, submenu_id: uuid.UUID) -> bool:
        """ delete single submenu by id from db """

        submenu = self.__get(
            submenu_id=submenu_id
        )

        if submenu:
            self.session.delete(submenu)
            return True

        return False


def get_submenu_dao(
        session: Session = Depends(get_db)
) -> SubmenuDao:
    return SubmenuDao(session=session)
