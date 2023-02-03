import uuid

from pydantic import BaseModel


class MenuBase(BaseModel):
    """
    base schema
    """
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuCreate(MenuBase):
    """
    create schema
    """
    pass


class MenuUpdate(BaseModel):
    """
    update schema
    """
    title: str | None = None
    description: str | None = None


class MenuRead(MenuBase):
    """
    read schema
    """
    id: uuid.UUID
    submenus_count: int = 0
    dishes_count: int = 0
