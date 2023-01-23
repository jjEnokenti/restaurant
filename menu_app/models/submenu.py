import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from menu_app.core.setup_db import Base


__all__ = [
    "Submenu"
]


class Submenu(Base):
    __tablename__ = "submenu_table"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))

    menu_id = Column(UUID(as_uuid=True), ForeignKey("menu_table.id", ondelete="CASCADE"))

    dish = relationship("Dish", back_populates="submenu", cascade="all, delete, delete-orphan")
    menu = relationship("Menu", back_populates="submenu")
