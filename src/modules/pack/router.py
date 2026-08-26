from fastapi import APIRouter, Depends, HTTPException
import httpx
from src.modules.pack.service import listAllPacks, createPack
from src.modules.pack.schemas import PackSchema
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

@pack_routes.post("/create-pack")
async def CreatePack(
    pack: PackSchema, 
    session: Session = Depends(get_session)
):
    result = await createPack(pack_schema=pack, session=session)
    return result