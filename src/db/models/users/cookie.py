from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.models.base import Base
from sqlalchemy import String
class Cookie(Base):
    __tablename__ = "cookie"
    value: Mapped[String] = mapped_column(String(500), nullable = False)
    refresh_value: Mapped[String] = mapped_column(String(800), nullable = False)

    user: Mapped["Users"] = relationship(back_populates = "cookie", lazy = 'joined')

__all__ = "Cookie"