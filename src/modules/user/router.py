from fastapi import APIRouter, Depends, HTTPException
import httpx
from src.modules.user.models import User
from src.modules.user.service import createUser, login, loginForm, use_refresh_token
from src.modules.user.schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.common.dependencies import get_session, verificate_token
from fastapi.security import OAuth2PasswordRequestForm



user_routes = APIRouter(prefix="/users", tags=["users"])


@user_routes.get("/")
async def user():
    return {"mensagem": "Você acessou a rota de usuário"}

@user_routes.post("/", response_model=None)
async def CreateUser(user:UserSchema, session: Session = Depends(get_session)):
    result = await createUser(user_schema=user, session=session)
    return result

@user_routes.post("/login", response_model=None)
async def Login(login_schema:LoginSchema, session: Session = Depends(get_session)):
    result = await login(login_schema=login_schema, session=session)
    return result

@user_routes.post("/login-form", response_model=None)
async def LoginForm(data_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    
    user_email = data_form.username 
    user_password = data_form.password
    
    dados_login = LoginSchema(email=user_email, password=user_password)
    
    result = await login(login_schema=dados_login, session=session)
    
    return result

@user_routes.get("/refresh")
async def UseRefreshToken(user:User = Depends(verificate_token)):
    result = await use_refresh_token(user=user)
    return result
