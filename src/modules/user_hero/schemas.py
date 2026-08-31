from pydantic import BaseModel
from typing import Optional

class UserHeroSchema(BaseModel):
    hero: int
    user: int
    level: int
    fragments: int
    active: Optional[bool]

    class Config:
        from_attributes = True