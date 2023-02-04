from fastapi import HTTPException, status, Depends
from sqlalchemy import func, distinct
from sqlalchemy.orm import Session

from menu_app.dependences import get_db
from menu_app.models import menu as m, dish as d, submenu as s

__all__ = (
    'get_menu_service',
    'MenuService',
)


class MenuService:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        """
        get all menus from db
        """
        try:
            menus_query = self.session.query(
                m.Menu.id,
                m.Menu.title,
                m.Menu.description,
                func.count(distinct(s.Submenu.id)).label('submenus_count'),
                func.count(d.Dish.id).label('dishes_count')
            ) \
                .group_by(m.Menu.id) \
                .outerjoin(s.Submenu, m.Menu.id == s.Submenu.menu_id) \
                .outerjoin(d.Dish, s.Submenu.id == d.Dish.submenu_id)

            menus = menus_query.all()

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')
        else:
            return menus

    def get_single_by_id(self, menu_id):
        """
        get single menu by id from db
        """
        try:
            menu_query = self.session.query(
                m.Menu.id,
                m.Menu.title,
                m.Menu.description,
                func.count(distinct(s.Submenu.id)).label('submenus_count'),
                func.count(d.Dish.id).label('dishes_count')
            ). \
                group_by(m.Menu.id). \
                outerjoin(s.Submenu, m.Menu.id == s.Submenu.menu_id). \
                outerjoin(d.Dish, d.Dish.submenu_id == s.Submenu.id). \
                filter(m.Menu.id == menu_id)

            menu = menu_query.first()

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')
        else:
            if not menu:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail='menu not found')

            return menu

    def create(self, create_data):
        """
        insert new menu into db
        """
        try:
            new_menu = m.Menu(**create_data.dict())
            self.session.add(new_menu)
            self.session.commit()
            self.session.refresh(new_menu)
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')
        else:
            return new_menu

    def update(self, menu_id, update_data):
        """
        update single menu by id into db
        """
        try:
            menu_query = self.session.query(m.Menu).filter(m.Menu.id == menu_id)
            updated_menu = menu_query.first()

            if not updated_menu:
                raise ValueError(f'menu with: id {menu_id} not found')

            menu_query.update(update_data.dict(exclude_unset=True))
            self.session.commit()
            self.session.refresh(updated_menu)
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')
        else:
            return updated_menu

    def delete(self, menu_id):
        """
        delete single menu by id from db
        """
        try:
            menu_query = self.session.query(m.Menu)
            menu = menu_query.get(menu_id)
            if not menu:
                raise ValueError(f'menu with: id {menu_id} not found')

            self.session.delete(menu)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'error message: {e}')


def get_menu_service(
        session: Session = Depends(get_db)
) -> MenuService:
    return MenuService(session=session)
