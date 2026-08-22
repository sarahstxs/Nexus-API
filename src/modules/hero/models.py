from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from src.core.database import Base

class Hero(Base):
    __tablename__ = "heroes"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False, unique=True)
    active = Column("active", Boolean, nullable=False, unique=False)
    name = Column("name", String(1000), nullable=False, unique=True)
    real_name = Column("real_name", String(100), nullable=False, unique=False)
    deck = Column("deck", String(5000), nullable=False, unique=True)
    gender = Column("gender", Integer, nullable=False, unique=False)
    origin = Column("origin", Integer, nullable=False, unique=False)
    birth = Column("birth", DateTime, nullable=True, unique=False)
    appearance = Column("apperance", Integer, nullable=False, unique=False)
    first_appearance_date = Column("first_appearance_date", DateTime, nullable=False, unique=False)
    first_appearance_comic = Column("first_appearance_comic", String(1000), nullable=False, unique=False)
    image_hero = Column("image_hero", String(1000), nullable=False, unique=True)
    nemesis = Column("nemesis", ForeignKey("heroes.id"), nullable=True, unique=False)
    rarity = Column("rarity", Integer, nullable=False, unique=False)
    class_hero = Column("class", Integer, ForeignKey("class_heroes.id"), nullable=False, unique=False)
    hyper_attack = Column("hyper_attack", Integer, ForeignKey("hyper_attacks.id"), nullable=False, unique=False)
    base_atk = Column("base_atk", Integer, nullable=False, unique=False)
    base_hp = Column("base_hp", Integer, nullable=False, unique=False)
    base_def = Column("base_def", Integer, nullable=False, unique=False)

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
