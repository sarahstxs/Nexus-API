from fastapi import APIRouter, Depends, HTTPException
import httpx
from src.modules.hyper_attack.service import listAllHyperAttacks, createHyperAttack, desativateHyperAttack, listHyperAttacks, activateHyperAttack
from src.modules.user.service import verificate_token
from src.modules.hyper_attack.schemas import HyperAttackSchema
from sqlalchemy.orm import Session
from src.common.dependencies import get_session

hyper_attack_routes = APIRouter(prefix="/hyper-attacks", tags=["hyper-attacks"])
#
@hyper_attack_routes.get("/")
async def class_hero():
    return {"mensagem": "Você acessou a rota de hiper ataques!"}

@hyper_attack_routes.get("/list")
async def ListAllHyperAttacks(session: Session = Depends(get_session)):
    result = await listAllHyperAttacks(session)
    return result

@hyper_attack_routes.get("/list/{id}")
async def ListClass(id_hyper_attack: int, session: Session = Depends(get_session)):
    result = await listHyperAttacks(id_hyper_attack=id_hyper_attack, session=session)
    return result

@hyper_attack_routes.post("/")
async def CreateHyperAttack(
    hyper_attack_schema: HyperAttackSchema, 
    session: Session = Depends(get_session),
    user = Depends(verificate_token) 
    ):
    result = await createHyperAttack(hyper_attack_schema=hyper_attack_schema, session=session, user=user)
    return result

@hyper_attack_routes.patch("/desativate/{id}")
async def DesativateHyperAttack(id_hyper_attack: int,
                      session: Session = Depends(get_session),
                      user = Depends(verificate_token) ):
    result = await desativateHyperAttack(id_hyper_attack=id_hyper_attack, session=session, user=user)
    return result

@hyper_attack_routes.patch("/activate/{id}")
async def ActivateClass(id_hyper_attack: int,
                      session: Session = Depends(get_session),
                      user = Depends(verificate_token) ):
    result = await activateHyperAttack(id_hyper_attack=id_hyper_attack, session=session, user=user)
    return result
