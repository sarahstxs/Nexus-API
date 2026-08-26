from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PackSchema(BaseModel):
    name: str
    deck: str

    class Config:
        from_attributes = True