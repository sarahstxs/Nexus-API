from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker
from src.modules.user.models import User
from sqlalchemy.orm import Session
from jose import jwt, JWTError
# from main import SECRET_KEY, ALGORITHM, oauth2_schema
from src.core.database import db

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
