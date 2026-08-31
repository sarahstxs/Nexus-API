from fastapi import APIRouter, Depends, HTTPException
import httpx
from src.modules.user_hero.service import loseHealth, acquireHealth, reviveHero
from src.modules.user.service import verificate_token
from src.modules.pack.schemas import PackSchema
from sqlalchemy.orm import Session
from src.common.dependencies import get_session

user_hero_routes = APIRouter(prefix="/user-heroes", tags=["user-heroes"])
#
@user_hero_routes.get("/")
async def pack():
    return {"mensagem": "Você acessou a rota de heróis do usuário!"}

@user_hero_routes.patch("/lose-health/{id_user}/{id_hero}/{damage}")
async def LoseHealth(id_hero: int,
                     id_user: int,
                     damage: int,
                     session: Session = Depends(get_session)
                     ):
    result = await loseHealth(session=session, id_hero=id_hero, id_user=id_user, damage=damage)
    return result

@user_hero_routes.patch("/acquire-health/{id_user}/{id_hero}/{health}")
async def AcquireHealth(id_hero: int,
                     id_user: int,
                     health: int,
                     session: Session = Depends(get_session)
                     ):
    result = await acquireHealth(session=session, id_hero=id_hero, id_user=id_user, health=health)
    return result

@user_hero_routes.patch("/revive-hero/{id_user}/{id_hero}")
async def ReviveHero(id_hero: int,
                     id_user: int,
                     session: Session = Depends(get_session)
                     ):
    result = await reviveHero(session=session, id_hero=id_hero, id_user=id_user)
    return result