from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.db.models.base import Base

#Base contains "is_active" boolean field, from the value of this field we calculate wether user is anonymous or not
class Users(Base):
    __tablename__ = "users"
    cookie_id: Mapped[String] = mapped_column(String(500), nullable = True)



__all__ = "users"