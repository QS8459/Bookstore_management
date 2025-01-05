from pydantic import BaseModel
from uuid import UUID
class UserSchema(BaseModel):
    id: str
    ip_address: str | None