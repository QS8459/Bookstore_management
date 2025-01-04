from pydantic import BaseModel
from uuid import UUID
class UserSchema(BaseModel):
    id: str
    cookie_id: str | None