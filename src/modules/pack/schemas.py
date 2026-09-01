from pydantic import BaseModel
from typing import Optional

class PackSchema(BaseModel):
    name: str
    deck: str
    active: Optional[bool]
    price: int

    class Config:
        from_attributes = True