from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from core.database import Base

class Place(Base):
    __tablename__ = "places"

    id = Column("id", Integer, primary_key=True, index=True, autoIncrement=True, nullable=False, unique=True)
    name = Column("name", String(50), nullable=False, unique=False)
    image = Column("image", String(max), nullable=False, unique=False)
    effect = Column("effect", Integer, nullable=False, unique=False)

    def __init__(self, name, image, effect):
        self.name = name
        self.image = image
        self.effect = effect