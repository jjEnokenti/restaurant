import uuid

from fastapi import Depends
from sqlalchemy import select, func, distinct
from sqlalchemy.engine import row
from sqlalchemy.orm import Session

from menuapp.dao.models import menu as m, submenu as s, dish as d
from menuapp.dao.schemas.menu import MenuCreate, MenuUpdate
from menuapp.dependences import get_db

__all__ = (
    'get_menu_dao',
    'MenuDao',
)


class MenuDao:
    menu_model: m.Menu = m.Menu
    submenu_model: s.Submenu = s.Submenu
    dish_model: d.Dish = d.Dish

    def __init__(self, session: Session):
        self.session = session

    def __get(self, menu_id: uuid.UUID) -> menu_model:
        """ get menu scalar data """

        statement = select(
            self.menu_model
        ).where(self.menu_model.id == menu_id)

        menu = self.session.execute(
            statement=statement
        ).scalar_one_or_none()

        return menu

    def get_all(self) -> list[row]:
        """ get all menus """

        statement = select(
            self.menu_model.id,
            self.menu_model.title,
            self.menu_model.description,
            func.count(distinct(self.submenu_model.id)).label('submenus_count'),
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

        menus = self.session.execute(
            statement=statement
        ).all()

        return menus

    def get_single_by_id(self, menu_id: uuid.UUID) -> row:
        """ get single menu by id """

        statement = select(
            self.menu_model.id,
            self.menu_model.title,
            self.menu_model.description,
            func.count(distinct(self.submenu_model.id)).label('submenus_count'),
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

        menu = self.session.execute(
            statement=statement
        ).one_or_none()

        return menu

    def create(self, data: MenuCreate) -> MenuCreate:
        """ insert new menu """

        new_menu = self.menu_model(**data.dict())
        self.session.add(new_menu)

        return new_menu

    def update(
            self,
            menu_id: uuid.UUID,
            data: MenuUpdate
    ) -> MenuUpdate | None:
        """ update single menu by id """

        updated_menu = self.__get(menu_id=menu_id)
        if updated_menu:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(updated_menu, key, value)
            self.session.add(updated_menu)

        return updated_menu

    def delete(self, menu_id: uuid.UUID) -> bool:
        """ delete single menu by id """
        menu = self.__get(menu_id=menu_id)

        if menu:
            self.session.delete(menu)
            return True

        return False


def get_menu_dao(
        session: Session = Depends(get_db)
) -> MenuDao:
    return MenuDao(session=session)