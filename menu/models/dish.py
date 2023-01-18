import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from menu.core import Base


class Dish(Base):
    __tablename__ = "dish"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))
    price = Column(String)

    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenu.id"))
