import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from src.modules.pack.schemas import PackSchema
from src.common.dependencies import get_session
from sqlalchemy.orm import Session
from src.modules.pack.models import Pack
from dotenv import load_dotenv

load_dotenv()

async def listAllPacks(session: Session):
    list = session.query(Pack).all()
    return {"Packs": list}

async def createPack(session, pack_schema, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para criar pacotes!")
    
    name = pack_schema.name,
    deck = pack_schema.deck
    active = pack_schema.active

    new_pack = {
        "name": name,
        "deck": deck,
        "active": active
    }
    
    final_pack = Pack(**new_pack)
    session.add(final_pack)
    session.commit()
    session.refresh(final_pack)
    return {"mensagem": f"Pacote cadastrado com sucesso "}

async def deletePack(session, id_pack, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para desativar esse pacote")
    
    pack = session.query(Pack).filter(Pack.id == id_pack).first()

    if not pack:
        raise HTTPException(status_code=404, detail="Pacote não encontrado!")
    
    pack.active = False
    session.commit()
    return {"mensagem": "Pacote desativado com sucesso!",
            "Pacote": pack}

async def listPack(session: Session, id_pack: int):
    pack = session.query(Pack).filter(Pack.id == id_pack).first()
    return pack