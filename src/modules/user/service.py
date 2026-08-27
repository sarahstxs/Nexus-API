import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from src.common.dependencies import get_session, verificate_token
from sqlalchemy.orm import Session
from src.modules.user.models import User
from src.modules.user.schemas import UserSchema, LoginSchema
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from src.core.config import bcrypt_context, ACESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm


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
    
async def login(login_schema: LoginSchema, session = Depends(get_session)):
    user = autenticate_user(login_schema.email, login_schema.password, session)

    if not user:
        raise HTTPException(status_code=400, detail= "Usuário não encontrado ou credenciais inválidas!")
    else:
        access_token = create_token(str(user.id))
        refresh_token = create_token(str(user.id), duration_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    
async def loginForm(data_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = autenticate_user(data_form.username, data_form.password, session)

    if not user:
        raise HTTPException(status_code=400, detail= "Usuário não encontrado ou credenciais inválidas!")
    else:
        access_token = create_token(str(user.id))
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    
async def use_refresh_token(user: User = Depends(verificate_token)):
    #Verificar token
    access_token = create_token(str(user.id))
    return {
            "access_token": access_token,
            "token_type": "Bearer"
        }