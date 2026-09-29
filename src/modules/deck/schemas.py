from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeckSchema(BaseModel):
    create_date: datetime
    user: int
    active: Optional[bool]

    class Config:
        from_attributes = True

class DeckCreateSchema(BaseModel):
    id_user: int
    id_hero1: int
    id_hero2: int
    id_hero3: int
    id_hero4: int
    id_hero5: int
    id_hero6: int