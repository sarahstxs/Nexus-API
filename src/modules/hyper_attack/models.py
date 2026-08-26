from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from src.core.database import Base

class HyperAttack(Base):
    __tablename__ = "hyper_attacks"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False, unique=True)
    name = Column("name", String(50), nullable=False, unique=True)
    effect = Column("effect", Integer, nullable=False, unique=False)
    required_energy = Column("required_energy", Integer, nullable=False, unique=False)
    active = Column("active", Boolean, nullable=False, unique=False)

    def __init__(self, name, effect, required_energy, active):
        self.name = name
        self.effect = effect
        self.required_energy = required_energy
        self.active = active