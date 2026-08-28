from fastapi import APIRouter, Depends, HTTPException
import httpx
from src.modules.user.models import User
from src.modules.user.service import createUser, login, loginForm, use_refresh_token, listActiveHyperAttackByName, listActiveUser, listAllUsers, listUSer, activateUser, desativateUser, upHighestLevel
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

@user_routes.get("/list-active")
async def ListActiveUser(session: Session = Depends(get_session)):
    result = await listActiveUser(session=session)
    return result

@user_routes.get("/list-active-name/{name_pack}")
async def ListActiveClassByName(name_user: str, session: Session = Depends(get_session)):
    result = await listActiveHyperAttackByName(session=session, name_user=name_user)
    return result

@user_routes.get("/list")
async def ListAllUsers(session: Session = Depends(get_session),user = Depends(verificate_token)):
    result = await listAllUsers(session, user=user)
    return result

@user_routes.get("/list/{id}")
async def ListUser(id_user: int, session: Session = Depends(get_session), user = Depends(verificate_token)):
    result = await listUSer(id_user=id_user, session=session, user=user)
    return result

@user_routes.patch("/desativate/{id}")
async def DesativateUser(id_user: int,
                      session: Session = Depends(get_session),
                      user = Depends(verificate_token) ):
    result = await desativateUser(id_user=id_user, session=session, user=user)
    return result

@user_routes.patch("/activate/{id}")
async def ActivateUser(id_user: int,
                      session: Session = Depends(get_session),
                      user = Depends(verificate_token) ):
    result = await activateUser(id_user=id_user, session=session, user=user)
    return result

@user_routes.patch("/up-level/{id}")
async def UpHighestLevel(id_user: int,
                      session: Session = Depends(get_session),
                      user = Depends(verificate_token) ):
    result = await upHighestLevel(id_user=id_user, session=session, user=user)
    return result