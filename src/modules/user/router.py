from fastapi import APIRouter, Depends, HTTPException
import httpx
from src.modules.user.models import User
from src.modules.user.service import createUser
from src.modules.user.schemas import UserSchema
from sqlalchemy.orm import Session
from src.common.dependencies import get_session


user_routes = APIRouter(prefix="/users", tags=["users"])


@user_routes.get("/")
async def user():
    return {"mensagem": "Você acessou a rota de usuário"}

@user_routes.post("/", response_model=None)
async def CreateUser(user:UserSchema, session: Session = Depends(get_session)):
    result = await createUser(user_schema=user, session=session)
    return result
