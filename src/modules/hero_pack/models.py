from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from src.core.database import Base

class HeroPack(Base):
    __tablename__ = "hero_packs"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False, unique=True)
    hero = Column("name", Integer, ForeignKey("heroes.id"), nullable=False, unique=False)
    pack = Column("pack", Integer, ForeignKey("packs.id"), nullable=False, unique=False)
    active = Column("active", Boolean, nullable=False, unique=False)

    def __init__(self, hero, pack, active):
        self.hero = hero
        self.pack = pack
        self.active = active