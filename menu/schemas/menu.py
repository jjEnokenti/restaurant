from pydantic import BaseModel, UUID4


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
    id: UUID4
    submenus_count: int = 0
    dishes_count: int = 0

