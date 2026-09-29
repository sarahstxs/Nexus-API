from pydantic import BaseModel

class BattleSchema(BaseModel):
    result: int

    class Config:
        from_attributes = True

class BattleActionSchema(BaseModel):
    user_hero_id: int          # ID do herói do jogador que vai agir
    action_type: str           # "basic", "special", "ultimate", "defend"
    target_enemy_index: int    # Índice do inimigo alvo (0 a 2)