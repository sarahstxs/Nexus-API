from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from core.database import Base

class classHero(Base):
    __tablename__ = "class_heroes"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, Nullable=False)
    name = Column("name", String(50), Nullable=False)
    special_attack_effect = Column("special_attack_effect", Integer, Nullable=False)
    special_attack_name = Column("special_attack_name", String(50), nullable=False)
    required_energy = Column("required_energy", Integer, Nullable=False)

    def __init__(self, name, special_attack_effect, special_attack_name, required_energy):
        self.name = name
        self.special_attack_effect = special_attack_effect
        self.special_attack_name = special_attack_name
        self.required_energy = required_energy