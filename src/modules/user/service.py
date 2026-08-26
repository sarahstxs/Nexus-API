import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from src.common.dependencies import get_session
from sqlalchemy.orm import Session
from src.modules.user.models import User
from src.modules.user.schemas import UserSchema
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from src.core.config import bcrypt_context, ACESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from jose import jwt, JWTError

load_dotenv()

def create_token(id_user: str, duration_token: int = timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + duration_token
    dic_info = {"sub": str(id_user), "exp": expiration_date}
    jwt_encoded = jwt.encode(dic_info, SECRET_KEY, ALGORITHM )

    return jwt_encoded

def autenticate_user(email: str, password:str, session):
    user = session.query(User).filter(User.email == email).first()

    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user 

async def createUser(user_schema: UserSchema, session = Depends(get_session)):

    usuario = session.query(User).filter(User.email == user_schema.email).first()

    if usuario:
        # Já existe usuário nessa sessão
        raise HTTPException(status_code=400, detail="Email de usuário já cadastrado")
    else:
        password = user_schema.password
        encrypted_password = bcrypt_context.hash(password)
        new_user = User(
            username=user_schema.username,
            password=encrypted_password,
            phone=user_schema.phone,
            email=user_schema.email,
            admin=user_schema.admin,
            active=user_schema.active,
            highest_level=user_schema.highest_level,
            coins=user_schema.coins,
            create_date=user_schema.create_date,
            current_level=user_schema.current_level
        )
        session.add(new_user)
        session.commit()
        return {"mensagem": f"Usuário {user_schema.username} cadastrado com sucesso "}
    
