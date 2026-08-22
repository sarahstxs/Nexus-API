from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from core.database import Base

class UserHero(Base):
        hero = Column("hero", Integer, ForeignKey("heroes.id"), nullable=False, unique=False)
        id = Column("id", Integer, primary_key=True, index=True, autoIncrement=True, nullable=False, unique=True)
        level = Column("level", Integer, nullable=False, unique=False)
        fragments = Column("fragments", Integer, nullable=False, unique=False)

        def __init__(self,hero, level=1, fragments=0):
                self.hero = hero
                self.level = level
                self.fragments = fragments