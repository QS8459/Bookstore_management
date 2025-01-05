from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from src.db.models.base import Base
from uuid import UUID
#Base contains "is_active" boolean field, from the value of this field we calculate wether user is anonymous or not
class Users(Base):
    __tablename__ = "users"
    cookie_id: Mapped[UUID] = mapped_column(ForeignKey("cookie.id"), nullable= True)
    ip_address: Mapped[String]= mapped_column(String(16), nullable = True)

    cookie: Mapped["Cookie"] = relationship(back_populates = 'user', lazy = 'selectin')


__all__ = "users"