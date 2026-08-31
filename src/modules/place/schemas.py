from pydantic import BaseModel
from typing import Optional

class PlaceSchema(BaseModel):
    name: str
    image: str
    effect: int
    active: Optional[bool]

    class Config:
        from_attributes = True