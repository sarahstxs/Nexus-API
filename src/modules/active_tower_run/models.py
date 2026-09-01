from sqlalchemy import Column, Integer, Boolean, ForeignKey
from src.core.database import Base

class ActiveTowerRun(Base):
    __tablename__ = "active_tower_runs"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False, unique=True)
    type_tower = Column("type_tower", Integer, nullable=False, unique=False)
    current_floor = Column("current_floor", Integer, nullable=False, unique=False)
    active_buff = Column("active_buff", Integer, nullable=False, unique=False)
    place = Column("place", Integer, ForeignKey("places.id"), nullable=False, unique=False)
    active = Column("active", Boolean, nullable=False, unique=False)

    def __init__(self, type_tower, current_floor, active_buff, place, active):
        self.type_tower = type_tower
        self.current_floor = current_floor
        self.active_buff = active_buff
        self.place = place
        self.active = active
