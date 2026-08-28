import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from src.modules.pack.schemas import PackSchema
from src.common.dependencies import get_session
from sqlalchemy.orm import Session
from src.modules.pack.models import Pack
from src.modules.hero_pack.models import HeroPack
from dotenv import load_dotenv

load_dotenv()

async def listAllPacks(session):
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

async def desativatePack(session, id_pack, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para desativar esse pacote")
    
    pack = session.query(Pack).filter(Pack.id == id_pack).first()

    if not pack:
        raise HTTPException(status_code=404, detail="Pacote não encontrado!")
    
    pack.active = False
    session.commit()
    return {"mensagem": "Pacote desativado com sucesso!",
            "Pacote": pack}

async def activatePack(session, id_pack, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para ativar esse pacote")
    
    pack = session.query(Pack).filter(Pack.id == id_pack).first()

    if not pack:
        raise HTTPException(status_code=404, detail="Pacote não encontrado!")
    
    pack.active = True
    session.commit()
    return {"mensagem": "Pacote ativado com sucesso!",
            "Pacote": pack}

async def listPack(session, id_pack):
    pack = session.query(Pack).filter(Pack.id == id_pack).first()
    return pack

async def listActivePack(session):
    pack = session.query(Pack).filter(Pack.active == True).all()
    return {"Packs": pack}

async def listActivePackByName(session, name_pack):
    packs = session.query(Pack).filter(
        Pack.name.icontains(name_pack),
        Pack.active == True
    ).all()
    
    return packs

async def listHeroPack(session, id_hero_pack):
    hero_pack = session.query(HeroPack).filter(HeroPack.id == id_hero_pack).first()
    return hero_pack

async def listAllHeroPack(session):
    list_hero_pack = session.query(HeroPack).all()
    return {"Hero_packs": list_hero_pack}