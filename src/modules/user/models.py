from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, PrimaryKeyConstraint, DateTime, Nullable
from src.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False, unique=True)
    username = Column("username", String(50), nullable=False, unique=True)
    password = Column("password", String(100), nullable=False, unique=False)
    phone = Column("phone", String(25), nullable=True, unique=True)
    email = Column("email", String(100), nullable=False, unique=True)
    admin = Column("admin", Boolean, nullable=False, unique=False, default=False)
    active = Column("active", Boolean,nullable=False, unique=False)
    highest_level = Column("highest_level", Integer, ForeignKey("active_tower_runs.id"), unique=False)
    coins = Column("coins", Integer, nullable=False, unique=False)
    create_date = Column("create_date", DateTime, nullable=False, unique=False)
    current_level = Column("current_level", Integer, ForeignKey("active_tower_runs.id"), nullable=False, unique=False)

    def __init__(self, username, password, phone, email, admin,active, highest_level, create_date, current_level, coins=300):
        self.username = username
        self.password = password
        self.phone = phone
        self.email = email
        self.admin = admin
        self.active = active
        self.highest_level = highest_level
        self.coins = coins
        self.create_date = create_date
        self.current_level = current_level
