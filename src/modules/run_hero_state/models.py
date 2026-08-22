from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from src.core.database import Base

class RunHEroState(Base):
    __tablename__ = "run_hero_states"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False, unique=True)
    current_hp = Column("current_hp", Integer, nullable=False, unique=False)
    drawback = Column("drawback", Integer, nullable=True, unique=False)
    alive = Column("alive", Boolean, nullable=False, unique=False)

    def __init__(self, current_hp, drawback, alive):
        self.current_hp = current_hp
        self.drawback = drawback
        self.alive = alive