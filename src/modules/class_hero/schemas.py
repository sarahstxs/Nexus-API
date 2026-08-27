from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClassSchema(BaseModel):
    name: str
    special_attack_effect: int
    special_attack_name: str
    required_energy: int
    active: Optional[bool]

    class Config:
        from_attributes = True