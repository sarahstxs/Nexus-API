from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeckSlotSchema(BaseModel):
    user_hero: int
    deck: int
    active: Optional[bool]

    class Config:
        from_attributes = True