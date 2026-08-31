from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from src.core.database import Base

class UserHero(Base):
        __tablename__ = "user_heroes"

        id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False, unique=True)
        hero = Column("hero", Integer, ForeignKey("heroes.id"), nullable=False, unique=False)
        user = Column("user", Integer, ForeignKey("users.id"), nullable=False, unique=False)
        level = Column("level", Integer, nullable=False, unique=False)
        fragments = Column("fragments", Integer, nullable=False, unique=False)
        active = Column("active", Boolean, nullable=False, unique=False)

        def __init__(self,hero, user, active, level=1, fragments=0):
                self.hero = hero
                self.user = user
                self.level = level
                self.fragments = fragments
                self.active = active