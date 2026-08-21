import os
from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from core.database import Base

class Hero(Base):
    __tablename__ = "heroes"

    id = Column("id", Integer, primary_key=True, index=True, autoIncrement=True, Nullable=False)
    name = Column("name", String(50), Nullable=False)
    real_name = Column("real_name", String(100), Nullable=False)
    deck = Column("deck", String(max), Nullable=False)
    gender = Column("gender", Integer, Nullable=False)
    origin = Column("origin", Integer, Nullable=False)
    birth = Column("birth", DateTime, Nullable=True)
    appearance = Column("apperance", Integer, Nullable=False)
    first_appearance_date = Column("first_appearance_date", DateTime, Nullable=False)
    first_appearance_comic = Column("first_appearance_comic", String(max), Nullable=False)
    image_hero = Column("image_hero", String(max), nullable=False)
    nemesis = Column("nemesis", ForeignKey("heroes.id"), nullable=True)
    rarity = Column("rarity", Integer, nullable=False)
    hyper_attack = Column("hyper_attack", Integer, ForeignKey("hyper_attacks.id"), nullable=False)
    base_atk = Column("base_atk", Integer)
    base_hp = Column("base_hp", Integer)
    base_def = Column("base_def", Integer)

    def __init__(self, name, real_name, deck, gender, origin, birth, apperance, first_appearance_date, first_appearance_comic, image_hero, nemesis, rarity, hyper_attack, base_atk, base_hp, base_def):
        self.name = name
        self.real_name = real_name
        self.deck = deck
        self.gender = gender
        self.origin = origin
        self.birth = birth
        self.apperance = apperance
        self.first_appearance_date = first_appearance_date
        self.first_appearance_comic = first_appearance_comic
        self.image_hero = image_hero
        self.nemesis = nemesis
        self.rarity = rarity
        self.hyper_attack = hyper_attack
        self.base_atk = base_atk
        self.base_hp = base_hp
        self.base_def = base_def
