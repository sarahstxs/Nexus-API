from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from core.database import Base

class Pack(Base):
    __tablename__ = "packs"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column("name", String(50), Nullable=False)
    deck = Column("deck", String(max), Nullable=False)

    def __init__(self, name, deck):
        self.name = name
        self.deck = deck