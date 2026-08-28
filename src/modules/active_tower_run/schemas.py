from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActiveTowerRunSchema(BaseModel):
    type_tower: int
    current_floor: int
    active_buff: int
    place: int
    active: Optional[bool]

    class Config:
        from_attributes = True