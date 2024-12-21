from src.db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Books(Base):
    __tablename__ = "books"
    title: Mapped[String] = mapped_column(String(100), nullable = False)
    year_published: Mapped[String] = mapped_column(DateTime, nullable = True)
    author_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid = True), ForeignKey('author.id', ondelete='CASCADE'), nullable = True)


    author: Mapped["Author"] = relationship(back_populates = "books", lazy="selectin")

__all__ =(
    'Books'
)