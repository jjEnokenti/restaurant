import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from menu.core import Base


class Menu(Base):
    __tablename__ = "menu_table"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))

    submenu = relationship("Submenu", back_populates="menu", cascade="all, delete-orphan")

    def __repr__(self):
        return f"{self.id}, {self.title}, {self.description}"
