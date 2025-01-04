from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.db.models.base import Base

class anonymous_user(Base):
    __tablename__ = "anonymous_user"
    cooke_id: Mapped[String] = mapped_column(String(500), nullable = False)


__all__ = "anonymous_user"