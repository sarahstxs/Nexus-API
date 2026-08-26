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

async def createPack(session: Session, pack_schema: PackSchema):
    name = pack_schema.name,
    deck = pack_schema.deck

    new_pack = {
        "name": name,
        "deck": deck
    }
    
    final_pack = Pack(**new_pack)
    session.add(final_pack)
    session.commit()
    session.refresh(final_pack)
    return {"mensagem": f"Pacote cadastrado com sucesso "}

async def deletePack(session: Session):
    