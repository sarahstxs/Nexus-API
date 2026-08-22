from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from src.core.database import Base
from datetime import datetime

class Deck(Base):
    __tablename__ = "decks"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False, unique=True)
    create_date = Column("create_date", DateTime, nullable=False, unique=False)
    user = Column("user", Integer, ForeignKey("users.id"), nullable=False, unique=False)

    def __init__(self, user, create_date: datetime = None):
        self.user = user
        self.create_date = create_date or datetime.now()