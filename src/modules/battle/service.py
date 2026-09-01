import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from src.modules.battle.schemas import BattleSchema
from src.modules.active_tower_run.schemas import ActiveTowerRunSchema
from src.common.dependencies import get_session
from sqlalchemy.orm import Session
from src.modules.battle.models import Battle
from datetime import datetime
from dotenv import load_dotenv

async def createBattle(session, id_deck, id_user, id_active_tower_run, battle_schema):
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

    return {"mensagem": "Batalha registrada com sucesso!"}

async def listAllBattles(session, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para desativar esse deck!")

    list = session.query(Battle).all()
    return {"Batalhas": list}

async def listBattle(session, id_battle, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para desativar esse deck!")
    battle = session.query(Battle).filter(Battle.id == id_battle).first()
    return battle

async def listBattlesByUser(session, user):
    battle = session.query(Battle).filter(Battle.user == user.id).all()
    return battle

async def listBattleByUser(session, user, id_battle):
    battle = session.query(Battle).filter(Battle.user == user.id, Battle.id == id_battle).first()
    return battle