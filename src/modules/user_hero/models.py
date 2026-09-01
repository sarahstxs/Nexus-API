from sqlalchemy import Column, Integer, Boolean, ForeignKey
from src.core.database import Base

class UserHero(Base):
        __tablename__ = "user_heroes"

        id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False, unique=True)
        hero = Column("hero", Integer, ForeignKey("heroes.id"), nullable=False, unique=False)
        user = Column("user", Integer, ForeignKey("users.id"), nullable=False, unique=False)
        current_hp = Column("current_hp", Integer, nullable=False, unique=False)
        max_hp = Column("max_hp", Integer, nullable=False, unique=False)
        drawback = Column("drawback", Integer, nullable=True, unique=False)
        alive = Column("alive", Boolean, nullable=False, unique=False)
        level = Column("level", Integer, nullable=False, unique=False)
        fragments = Column("fragments", Integer, nullable=False, unique=False)
        active = Column("active", Boolean, nullable=False, unique=False)

        def __init__(self,hero, user, active, current_hp, max_hp, drawback, alive, level=1, fragments=0):
                self.hero = hero
                self.user = user
                self.current_hp = current_hp
                self.max_hp = max_hp
                self.alive = alive
                self.drawback = drawback
                self.level = level
                self.fragments = fragments
                self.active = active