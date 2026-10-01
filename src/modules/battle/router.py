from fastapi import APIRouter, Depends
from src.modules.battle.service import createBattle, listAllBattles, listBattle, listBattleByUser, listBattlesByUser
from src.modules.user.service import verificate_token
from src.modules.battle.schemas import BattleSchema
from sqlalchemy.orm import Session
from src.common.dependencies import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_session
from src.modules.battle.schemas import BattleActionSchema
from src.modules.battle import service

battle_routes = APIRouter(prefix="/battles", tags=["battles"])

@battle_routes.get("/")
async def battle():
    return {"mensagem": "Você acessou a rota de batalhas!"}

@battle_routes.post("/")
async def CreateBattle(
    id_user: int,
    id_deck: int,
    id_active_tower_run: int,
    battle_schema: BattleSchema,
    session: Session = Depends(get_session)
    ):
    result = await createBattle(
        id_user=id_user, 
        id_deck=id_deck, 
        id_active_tower_run=id_active_tower_run,
        battle_schema=battle_schema,
        session=session)
    return result

@battle_routes.get("/list")
async def ListAllBattles(
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
    ):
    result = await listAllBattles(
        session=session,
        user=user)
    return result

@battle_routes.get("/list/{id}")
async def ListBattle(
    id_battle: int,
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
    ):
    result = await listBattle(
        id_battle=id_battle,
        session=session,
        user=user)
    return result

@battle_routes.get("/list-decks")
async def ListBattlesByUser(
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
    ):
    result = await listBattlesByUser(
        session=session,
        user=user)
    return result

@battle_routes.get("/list-user/{id_deck}")
async def ListBattleByUser(
    id_battle: int,
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
    ):
    result = await listBattleByUser(
        id_battle=id_battle,
        session=session,
        user=user)
    return result

@battle_routes.post("/start")
async def start_battle(
    floor: int, 
    place_id: int, 
    hero1: int, 
    hero2: int, 
    hero3: int, 
    hero4: int, 
    hero5: int, 
    hero6: int, 
    session: Session = Depends(get_session), 
    user = Depends(verificate_token)
):
    return await service.startBattle(session, user.id, floor, place_id, [hero1, hero2, hero3, hero4, hero5, hero6])

@battle_routes.post("/turn")
async def process_turn(
    action: BattleActionSchema, 
    state_data: dict, 
    session: Session = Depends(get_session), 
    user = Depends(verificate_token)
):
    return await service.processTurn(session, user.id, action, state_data)

@battle_routes.post("/start")
async def start_battle(
    floor: int, 
    place_id: int, 
    hero1: int, 
    hero2: int, 
    hero3: int, 
    hero4: int, 
    hero5: int, 
    hero6: int, 
    session: Session = Depends(get_session), 
    user = Depends(verificate_token)
):
    return await service.startBattle(session, user.id, floor, place_id, [hero1, hero2, hero3, hero4, hero5, hero6])