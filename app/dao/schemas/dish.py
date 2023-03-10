import uuid

from pydantic import BaseModel

__all__ = (
    "DishCreate",
    "DishRead",
    "DishUpdate"
)


class DishBase(BaseModel):
    """
    base schema
    """
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True


class DishCreate(DishBase):
    """
    create schema
    """
    pass


class DishUpdate(BaseModel):
    """
    update schema
    """
    title: str | None = None
    description: str | None = None
    price: str | None = None


class DishRead(DishBase):
    """
    read schema
    """
    id: uuid.UUID
