from sqlalchemy import Column, String, Integer, Boolean
from src.core.database import Base

class Pack(Base):
    __tablename__ = "packs"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False, unique=True)
    name = Column("name", String(50), nullable=False, unique=True)
    deck = Column("deck", String(5000), nullable=False, unique=True)
    active = Column("active", Boolean, nullable=False, unique=False)
    price = Column("price", Integer, nullable=False, unique=False)

    def __init__(self, name, deck, active, price):
        self.name = name
        self.deck = deck
        self.active = active
        self.price = price