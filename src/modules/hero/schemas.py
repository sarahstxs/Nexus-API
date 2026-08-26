from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HeroSchemaUser(BaseModel):
    id: int
    active: Optional[bool]
    nemesis: int
    rarity: int
    class_hero: int
    hyper_attack: int
    base_atk: int
    base_hp: int
    base_def: int

    class Config:
        from_attributes = True

class HeroSchemaApi(BaseModel):
    name: str
    real_name: str
    deck: str
    gender: int
    origin: int
    birth: str
    appearance: int
    first_appearance_comic: str
    image_hero: str

    class Confuig:
        from_atributes = True