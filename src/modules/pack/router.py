from fastapi import APIRouter, Depends, HTTPException
import httpx
from src.modules.pack.service import listAllPacks, createPack, deletePack, listPack
from src.modules.pack.schemas import PackSchema
from sqlalchemy.orm import Session
from src.common.dependencies import get_session

pack_routes = APIRouter(prefix="/packs", tags=["pack"])

@pack_routes.get("/")
async def hero():
    return {"mensagem": "Você acessou a rota de pacotes!"}

@pack_routes.get("/")
async def listPacks(session: Session = Depends(get_session)):
    result = await listAllPacks(session)
    return result

@pack_routes.get("/{id}")
async def ListPack(id_pack: int, session: Session = Depends(get_session)):
    result = await listPack(id_pack=id_pack, session=session)
    return result

@pack_routes.post("/")
async def CreatePack(
    pack: PackSchema, 
    session: Session = Depends(get_session)):
    result = await createPack(pack_schema=pack, session=session)
    return result

@pack_routes.patch("/{id}")
async def DeletePack(id_pack: int, session: Session = Depends(get_session)):
    result = await deletePack(id_pack=id_pack, session=session)
    return result

