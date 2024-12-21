from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String
from src.db.models.base import Base
class Author(Base):
    __tablename__ = "author"

    first_name: Mapped[String] = mapped_column(String(150), nullable = False)
    last_name: Mapped[String] = mapped_column(String(150), nullable = False)
    middle_name: Mapped[String] = mapped_column(String(150), nullable = True)
    books: Mapped["Books"] = relationship(back_populates = "author", lazy = 'joined')



__all__ = "Author"