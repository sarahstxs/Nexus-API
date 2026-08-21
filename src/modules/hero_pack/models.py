from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from core.database import Base

class HeroPack(Base):
    __tablename__ = "hero_pack"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, Nullable=False)
    hero = Column("name", Integer, ForeignKey("heroes.id"), Nullable=False)
    pack = Column("pack", Integer, ForeignKey("packs.id"), Nullable=False)

    def __init__(self, hero, pack):
        self.hero = hero
        self.pack = pack