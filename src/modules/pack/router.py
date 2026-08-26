from fastapi import APIRouter, Depends, HTTPException
import httpx
from src.modules.pack.service import listAllPacks
from src.modules.hero.schemas import HeroSchemaUser
from sqlalchemy.orm import Session
from src.common.dependencies import get_session

pack_routes = APIRouter(prefix="/pack", tags=["pack"])

@pack_routes.get("/")
async def hero():
    return {"mensagem": "Você acessou a rota de pacotes!"}

@pack_routes.get("/list-all-packs")
async def listPacks(session: Session = Depends(get_session)):
    result = await listAllPacks(session)
    return result