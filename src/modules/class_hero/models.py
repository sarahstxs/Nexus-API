from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from src.core.database import Base

class classHero(Base):
    __tablename__ = "class_heroes"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False, unique=True)
    name = Column("name", String(50), nullable=False, unique=True)
    special_attack_effect = Column("special_attack_effect", Integer, nullable=False, unique=True)
    special_attack_name = Column("special_attack_name", String(50), nullable=False, unique=True)
    required_energy = Column("required_energy", Integer, nullable=False, unique=False)
    active = Column("active", Boolean, nullable=False, unique=False)

    def __init__(self, name, special_attack_effect, special_attack_name, required_energy, active):
        self.name = name
        self.special_attack_effect = special_attack_effect
        self.special_attack_name = special_attack_name
        self.required_energy = required_energy
        self.active = active