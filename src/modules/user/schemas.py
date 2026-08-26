from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserSchema(BaseModel):
    username: str
    password: str
    phone: str
    email: str
    admin: Optional[bool]
    active: Optional[bool]
    highest_level: int
    coins: int
    create_date: datetime
    current_level: int

    class Config:
        from_attributes = True

