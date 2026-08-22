from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from src.core.database import Base

class Pack(Base):
    __tablename__ = "packs"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False, unique=True)
    name = Column("name", String(50), nullable=False, unique=True)
    deck = Column("deck", String(5000), nullable=False, unique=True)

    def __init__(self, name, deck):
        self.name = name
        self.deck = deck