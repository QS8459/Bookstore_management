
from pydantic import BaseModel, UUID4, AwareDatetime
from datetime import datetime
class BookBaseSchema(BaseModel):
    title: str
    year_published: datetime | None

class BookDetail(BookBaseSchema):
    year_published: datetime | None
    author: object
    id: UUID4
    created_at: datetime
    updated_at: datetime
    is_active: bool
