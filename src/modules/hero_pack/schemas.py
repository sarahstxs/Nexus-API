from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HeroPackSchema(BaseModel):
    pack: int
    active: Optional[bool]

    class Config:
        from_attributes = True