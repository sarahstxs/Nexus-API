from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from src.core.database import Base

class DeckSlot(Base):
    __tablename__ = "deck_slots"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False, unique=True)
    user_hero = Column("user_hero", Integer, ForeignKey("user_heroes.id"), nullable=False, unique=False)
    deck = Column("deck", Integer, ForeignKey("decks.id"), nullable=False, unique=False)

    def __init__(self, user_hero, deck):
        self.user_hero = user_hero
        self.deck = deck