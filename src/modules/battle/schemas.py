from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BattleSchema(BaseModel):
    result: int

    class Config:
        from_attributes = True