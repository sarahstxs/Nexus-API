from pydantic import BaseModel

class BattleSchema(BaseModel):
    result: int

    class Config:
        from_attributes = True