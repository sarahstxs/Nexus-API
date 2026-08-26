from fastapi import APIRouter, Depends, HTTPException
import httpx
from src.modules.hero.service import listAllHeroes, createHero
from src.modules.hero.schemas import HeroSchemaUser
from sqlalchemy.orm import Session
from src.common.dependencies import get_session

hero_routes = APIRouter(prefix="/hero", tags=["hero"])

@hero_routes.get("/")
async def hero():
    return {"mensagem": "Você acessou a rota de heróis!"}

@hero_routes.get("/list-all-heroes")
async def listHeroes():
    result = await listAllHeroes(10)
    return result

@hero_routes.post("/create-hero")
async def CreateHero(
    hero: HeroSchemaUser, 
    session: Session = Depends(get_session)
):
    result = await createHero(hero_schema_user=hero, session=session)
    return result