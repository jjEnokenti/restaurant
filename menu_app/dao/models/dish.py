import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from menu_app.core.setup_db import Base


__all__ = [
    "Dish"
]


class Dish(Base):
    __tablename__ = "dish_table"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))
    price = Column(String)

    submenu_id = Column(
        UUID(as_uuid=True),
        ForeignKey("submenu_table.id", ondelete="CASCADE")
    )

    submenu = relationship("Submenu", back_populates="dish")
