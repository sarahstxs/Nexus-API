import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from src.modules.pack.schemas import PackSchema
from src.common.dependencies import get_session
from sqlalchemy.orm import Session
from src.modules.place.models import Place
from src.modules.hero_pack.models import HeroPack
from dotenv import load_dotenv

load_dotenv()

async def listAllPlaces(session):
    list = session.query(Place).all()
    return {"Places": list}

async def createPlace(session, place_schema, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para criar lugares!")
    
    name = place_schema.name
    image = place_schema.image
    effect = place_schema.effect
    active = place_schema.active

    new_place = {
        "name": name,
        "image": image,
        "effect": effect,
        "active": active
    }
    
    final_place = Place(**new_place)
    session.add(final_place)
    session.commit()
    session.refresh(final_place)
    return {"mensagem": f"Lugar cadastrado com sucesso "}

async def desativatePlace(session, id_place, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para desativar esse lugar")
    
    place = session.query(Place).filter(Place.id == id_place).first()

    if not place:
        raise HTTPException(status_code=404, detail="Lugar não encontrado!")
    
    place.active = False
    session.commit()
    return {"mensagem": "Lugar desativado com sucesso!",
            "Lugar": place}

async def activatePlace(session, id_place, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para ativar esse lugar")
    
    place = session.query(Place).filter(Place.id == id_place).first()

    if not place:
        raise HTTPException(status_code=404, detail="Pacote não encontrado!")
    
    place.active = True
    session.commit()
    return {"mensagem": "Lugar ativado com sucesso!",
            "Lugar": place}

async def listPlace(session, id_place):
    place = session.query(Place).filter(Place.id == id_place).first()
    return place

async def listActivePlace(session):
    place = session.query(Place).filter(Place.active == True).all()
    return {"Lugar": place}

async def listActivePackByName(session, name_place):
    place = session.query(Place).filter(
        Place.name.icontains(name_place),
        Place.active == True
    ).all()
    
    return place