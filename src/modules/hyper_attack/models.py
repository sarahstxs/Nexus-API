import os
from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from core.database import Base

class HyperAttack(Base):
    __tablename__ = "hyper_attacks"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, Nullable=False)
    name = Column("name", String(50), Nullable=False)
    effect = Column("effect", Integer, Nullable=False)
    required_energy = Column("required_energy", Integer, Nullable=False)

    def __init__(self, name, effect, required_energy):
        self.name = name
        self.effect = effect
        self.required_energy = required_energy