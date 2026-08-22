from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from core.database import Base
from datetime import datetime

class Battle(Base):
    id = Column("id", Integer, primary_key=True, index=True, autoIncrement=True, nullable=False, unique=True)
    date = Column("date", DateTime, nullable=False, unique=False)
    floor_reached = Column("floor_reached", Integer, ForeignKey("active_tower_runs.id"), nullable=False, unique=False)
    deck = Column("deck", Integer, ForeignKey("decks.id"), nullable=False, unique=False)
    result = Column("result", Integer, nullable=False, unique=False)

    def __init__(self, floor_reached, deck, result, date: datetime = None):
        self.date = date or datetime.now()
        self.floor_reached = floor_reached
        self.deck = deck
        self.result = result