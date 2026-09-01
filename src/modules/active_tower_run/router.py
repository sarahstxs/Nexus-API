from fastapi import APIRouter, Depends
from src.modules.active_tower_run.service import listActiveActiveTowerRun, listActiveTowerRun, listAllActiveTowerRun, desativateActiveTowerRun, activateActiveTowerRun, createActiveTowerRun
from src.modules.active_tower_run.schemas import ActiveTowerRunSchema
from sqlalchemy.orm import Session
from src.common.dependencies import get_session, verificate_token

active_tower_run_routes = APIRouter(prefix="/active-tower-runs", tags=["active-tower-runs"])

@active_tower_run_routes.get("/")
async def ActiveTowerRun():
    return {"mensagem": "Você acessou a rota de níveis da torre!"}

@active_tower_run_routes.get("/list")
async def ListAllActiveTowerRun(
    session: Session = Depends(get_session)
    ):
    result = await listAllActiveTowerRun(
        session)
    return result

@active_tower_run_routes.get("/list/{id}")
async def ListActiveTowerRun(
    id_active_tower_run: int, 
    session: Session = Depends(get_session)
    ):
    result = await listActiveTowerRun(
        session,
        id_active_tower_run)   
    return result

@active_tower_run_routes.post("/")
async def CreateActiveTowerRun(
    active_tower_run: ActiveTowerRunSchema, 
    session: Session = Depends(get_session),
    user = Depends(verificate_token) 
    ):
    result = await createActiveTowerRun(
        active_tower_run_schema=active_tower_run,
        session=session,
        user=user)
    return result

@active_tower_run_routes.patch("/desativate/{id}")
async def DesativateActiveTowerRun(
    id_active_tower_run: int,
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
    ):
    result = await desativateActiveTowerRun(
        id_active_tower_run=id_active_tower_run,
        session=session,
        user=user)
    return result

@active_tower_run_routes.patch("/activate/{id}")
async def ActivateActiveTowerRun(
    id_active_tower_run: int,
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
    ):
    result = await activateActiveTowerRun(
        id_active_tower_run=id_active_tower_run, 
        session=session, 
        user=user)
    return result

@active_tower_run_routes.get("/list-active")
async def ListActiveActiveTowerRun(
    session: Session = Depends(get_session)
    ):
    result = await listActiveActiveTowerRun(
        session=session)
    return result
