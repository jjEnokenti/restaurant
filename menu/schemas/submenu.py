import uuid

from pydantic import BaseModel


class SubmenuBase(BaseModel):
    """
    base schema
    """
    title: str
    description: str | None = None

    class Config:
        orm_mode = True


class SubmenuCreate(SubmenuBase):
    """
    create schema
    """
    pass


class SubmenuUpdate(BaseModel):
    """
    update schema
    """
    title: str | None = None
    description: str | None = None


class SubmenuRead(SubmenuBase):
    """
    read schema
    """
    id: uuid.UUID
    dishes_count: int | None = 0
