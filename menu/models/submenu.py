import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from menu.core import Base


class Submenu(Base):
    __tablename__ = "submenu"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))

    menu_id = Column(UUID(as_uuid=True), ForeignKey("menu.id"))

    dish = relationship("Dish", cascade="all, delete", lazy='joined')
