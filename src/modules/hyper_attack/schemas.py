from pydantic import BaseModel
from typing import Optional

class HyperAttackSchema(BaseModel):
    name: str
    effect: int
    required_energy: int
    active: Optional[bool]

    class Config:
        from_attributes = True