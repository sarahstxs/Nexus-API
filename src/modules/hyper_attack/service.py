import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from src.modules.hyper_attack.schemas import HyperAttackSchema
from src.common.dependencies import get_session
from sqlalchemy.orm import Session
from src.modules.hyper_attack.models import HyperAttack
from dotenv import load_dotenv

load_dotenv()

async def listAllHyperAttacks(session):
    list = session.query(HyperAttack).all()
    return {"Hiper ataque": list}

async def listHyperAttacks(session, id_hyper_attack):
    hyper_attack = session.query(HyperAttack).filter(HyperAttack.id == id_hyper_attack).first()
    return hyper_attack

async def createHyperAttack(session, hyper_attack_schema, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para criar hiper ataques!")
    
    name = hyper_attack_schema.name,
    effect = hyper_attack_schema.effect
    required_energy = hyper_attack_schema.required_energy
    active = hyper_attack_schema.active

    new_hyper_atack = {
        "name": name,
        "effect": effect,
        "required_energy": required_energy,
        "active": active
    }
    
    final_hyper_attack = HyperAttack(**new_hyper_atack)
    session.add(final_hyper_attack)
    session.commit()
    session.refresh(final_hyper_attack)
    return {"mensagem": f"Hiper ataque cadastrada com sucesso "}

async def desativateHyperAttack(session, id_hyper_attack, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para desativar esse hiper ataque")
    
    hyper_attack = session.query(HyperAttack).filter(HyperAttack.id == id_hyper_attack).first()

    if not hyper_attack:
        raise HTTPException(status_code=404, detail="Hiper ataque não encontrada=o!")
    
    hyper_attack.active = False
    session.commit()
    return {"mensagem": "Hiper ataque desativado com sucesso!",
            "Classe": hyper_attack}

async def activateHyperAttack(session, id_hyper_attack, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para ativar essa classe!")
    
    hyper_attack = session.query(HyperAttack).filter(HyperAttack.id == id_hyper_attack).first()

    if not hyper_attack:
        raise HTTPException(status_code=404, detail="Hiper ataque não encontrado!")
    
    hyper_attack.active = True
    session.commit()
    return {"mensagem": "Hiper ataque ativado com sucesso!",
            "Hiper Ataque": hyper_attack}

async def listActiveHyperAttack(session):
    hyper_attack = session.query(HyperAttack).filter(HyperAttack.active == True).all()
    return hyper_attack

async def listActiveHyperAttackByName(session, name_hyper_attack):
    hyper_attack = session.query(HyperAttack).filter(
        HyperAttack.name.icontains(name_hyper_attack),
        HyperAttack.active == True
    ).all()
    
    return hyper_attack