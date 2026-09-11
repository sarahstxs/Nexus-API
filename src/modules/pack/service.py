from fastapi import  HTTPException
from sqlalchemy.orm import Session
from src.modules.pack.models import Pack
from src.modules.hero_pack.models import HeroPack
from dotenv import load_dotenv

load_dotenv()

async def listAllPacks(
        session):
    list = session.query(Pack).all()
    return {"Packs": list}

async def createPack(
        session, 
        pack_schema, 
        user):
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to create packs!")
    
    name = pack_schema.name,
    deck = pack_schema.deck
    active = pack_schema.active
    price = pack_schema.price

    new_pack = {
        "name": name,
        "deck": deck,
        "active": active,
        "price": price
    }
    
    final_pack = Pack(**new_pack)
    session.add(final_pack)
    session.commit()
    session.refresh(final_pack)
    return {"message": f"Pack registered successfully!"}

async def desativatePack(
        session, 
        id_pack, 
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to deactivate this pack!")
    
    pack = session.query(Pack).filter(Pack.id == id_pack).first()

    if not pack:
        raise HTTPException(
            status_code=404, 
            detail="Pack not found!")
    
    pack.active = False
    session.commit()
    return {"message": "Pack deactivated successfully!",
            "Pack": pack}

async def activatePack(
        session, 
        id_pack, 
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to activate this pack!")
    
    pack = session.query(Pack).filter(Pack.id == id_pack).first()

    if not pack:
        raise HTTPException(
            status_code=404, 
            detail="Pack not found!")
    
    pack.active = True
    session.commit()
    return {"message": "Pack activated successfully!",
            "Pack": pack}

async def listPack(
        session, 
        id_pack):
    pack = session.query(Pack).filter(Pack.id == id_pack).first()
    return pack

async def listActivePack(
        session):
    pack = session.query(Pack).filter(Pack.active == True).all()
    return {"Packs": pack}

async def listActivePackByName(
        session, 
        name_pack):
    packs = session.query(Pack).filter(
        Pack.name.icontains(name_pack),
        Pack.active == True
    ).all()
    
    return packs

async def listHeroPack(
        session, 
        id_hero_pack):
    hero_pack = session.query(HeroPack).filter(HeroPack.id == id_hero_pack).first()
    return hero_pack

async def listAllHeroPack(
        session):
    list_hero_pack = session.query(HeroPack).all()
    return {"Hero_packs": list_hero_pack}