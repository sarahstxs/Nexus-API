from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PackSchema(BaseModel):
    name: str
    deck: str
    active: Optional[bool]

    class Config:
        from_attributes = True