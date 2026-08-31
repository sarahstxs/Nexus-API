from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeckSchema(BaseModel):
    create_date: datetime
    user: int
    active: Optional[bool]

    class Config:
        from_attributes = True