from pydantic import BaseModel
class UserSchema(BaseModel):
    id: str
    ip_address: str | None