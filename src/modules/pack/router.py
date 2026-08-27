from fastapi import APIRouter, Depends, HTTPException
import httpx
from src.modules.pack.service import listAllPacks, createPack, desativatePack, listPack, listHeroPack, listAllHeroPack, activatePack
from src.modules.user.service import verificate_token
from src.modules.pack.schemas import PackSchema
from sqlalchemy.orm import Session
from src.common.dependencies import get_session

pack_routes = APIRouter(prefix="/packs", tags=["packs"])
#
@pack_routes.get("/")
async def pack():
    return {"mensagem": "Você acessou a rota de pacotes!"}

@pack_routes.get("/list")
async def ListAllPacks(session: Session = Depends(get_session)):
    result = await listAllPacks(session)
    return result

@pack_routes.get("/list/{id}")
async def ListPack(id_pack: int, session: Session = Depends(get_session)):
    result = await listPack(id_pack=id_pack, session=session)
    return result

@pack_routes.post("/")
async def CreatePack(
    pack: PackSchema, 
    session: Session = Depends(get_session),
    user = Depends(verificate_token) 
    ):
    result = await createPack(pack_schema=pack, session=session, user=user)
    return result

@pack_routes.patch("/desativate/{id}")
async def DesativatePack(id_pack: int,
                      session: Session = Depends(get_session),
                      user = Depends(verificate_token) ):
    result = await desativatePack(id_pack=id_pack, session=session, user=user)
    return result

@pack_routes.patch("/activate/{id}")
async def ActivatePack(id_pack: int,
                      session: Session = Depends(get_session),
                      user = Depends(verificate_token) ):
    result = await activatePack(id_pack=id_pack, session=session, user=user)
    return result

##############* Hero_pack *#######################

@pack_routes.get("/list-hero-pack/{id}")
async def ListHeroPack(id_hero_pack: int,
                        session: Session = Depends(get_session)):
    result = await listHeroPack(session=session, id_hero_pack=id_hero_pack)
    return result

@pack_routes.get("list-All-hero-pack")
async def ListAllHero(session: Session = Depends(get_session)):
    result = await listAllHeroPack(session=session)
    return result