from menu.core import db, Base
from menu.models import Menu, Submenu, Dish  # noqa


def init_db():
    Base.metadata.drop_all(db)
    Base.metadata.create_all(db)
