from src.db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
class History(Base):
    __tablename__ = "history"
    action: Mapped[String] = mapped_column(String(20), nullable = True)
    fields: Mapped[String] = mapped_column(String(10000), nullable = True)
    model: Mapped[String] = mapped_column(String(30), nullable = True)


__all__ = "History"