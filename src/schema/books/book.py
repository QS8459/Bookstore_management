from pydantic import BaseModel, UUID4, AwareDatetime
from datetime import datetime
from typing import Optional
class BookBaseSchema(BaseModel):
    title: str
    year_published: Optional[datetime] =None

class BookUpdateSchema(BookBaseSchema):
    id: UUID4
class BookDetailSchema(BookBaseSchema):
    year_published: Optional[datetime] = None
    author: object
    id: UUID4
    created_at: datetime
    updated_at: datetime
    is_active: bool

