from fastapi import HTTPException
from src.modules.battle.models import Battle
from datetime import datetime

async def createBattle(
        session,
        id_deck,
        id_user,
        id_active_tower_run,
        battle_schema):
    date = datetime.now()
    floor_reached = id_active_tower_run
    deck = id_deck
    result = battle_schema.result
    user = id_user

    new_battle = {
        "date": date,
        "floor_reached": floor_reached,
        "deck": deck,
        "result": result,
        "user": user
    }
    final_battle = Battle(**new_battle)
    session.add(final_battle)
    session.commit()
    session.refresh(final_battle)

    return {"message": "Battle registered successfully!"}

async def listAllBattles(
        session,
        user):
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to deactivate this battle!")

    list = session.query(Battle).all()
    return {"Battles": list}

async def listBattle(
        session,
        id_battle,
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to list this battle!")
    
    battle = session.query(Battle).filter(Battle.id == id_battle).first()
    return battle

async def listBattlesByUser(
        session,
        user):
    battle = session.query(Battle).filter(Battle.user == user.id).all()
    return battle

async def listBattleByUser(
        session,
        user,
        id_battle):
    battle = session.query(Battle).filter(Battle.user == user.id, Battle.id == id_battle).first()
    return battle