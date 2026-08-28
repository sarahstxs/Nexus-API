from fastapi import APIRouter, Depends, HTTPException
import httpx
from src.modules.user.models import User
from src.modules.user.service import createUser, login, loginForm, use_refresh_token, listActiveHyperAttackByName, listActiveUser, listAllUsers, listUSer
from src.modules.user.schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.common.dependencies import get_session, verificate_token
from fastapi.security import OAuth2PasswordRequestForm



active_tower_run = APIRouter(prefix="/active-tower-runs", tags=["active-tower-runs"])


@active_tower_run.get("/")
async def ActiveTowerRun():
    return {"mensagem": "Você acessou a rota de níveis da torre!"}