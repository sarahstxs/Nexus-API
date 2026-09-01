from fastapi import HTTPException
from src.modules.active_tower_run.models import ActiveTowerRun

async def listAllActiveTowerRun(session):
    list = session.query(ActiveTowerRun).all()
    return {"Níveis da torre": list}

async def listActiveTowerRun(session, id_active_tower_run):
    active_tower_run = session.query(ActiveTowerRun).filter(ActiveTowerRun.id == id_active_tower_run).first()
    return active_tower_run

async def createActiveTowerRun(session, active_tower_run_schema, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para criar níveis da torre!")
    
    type_tower = active_tower_run_schema.type_tower
    current_floor = active_tower_run_schema.current_floor
    active_buff = active_tower_run_schema.active_buff
    place = active_tower_run_schema.place
    active = active_tower_run_schema.active

    new_active_tower_run = {
        "type_tower": type_tower,
        "current_floor": current_floor,
        "active_buff": active_buff,
        "place": place,
        "active": active
    }
    
    final_active_tower_run = ActiveTowerRun(**new_active_tower_run)
    session.add(final_active_tower_run)
    session.commit()
    session.refresh(final_active_tower_run)
    return {"mensagem": f"Nível da torre cadastrado com sucesso "}

async def desativateActiveTowerRun(session, id_active_tower_run, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para desativar níveis da torre!")
    
    active_tower_run = session.query(ActiveTowerRun).filter(ActiveTowerRun.id == id_active_tower_run).first()

    if not active_tower_run:
        raise HTTPException(status_code=404, detail="Nível da torre não encontrado!")
    
    active_tower_run.active = False
    session.commit()
    return {"mensagem": "Nível da torre desativado com sucesso!",
            "Nível da torre": active_tower_run}

async def activateActiveTowerRun(session, id_active_tower_run, user):
    if not user.admin:
        raise HTTPException(status_code=403,detail="Você não tem permissão para ativar esse nível da torre!")
    
    active_tower_run = session.query(ActiveTowerRun).filter(ActiveTowerRun.id == id_active_tower_run).first()

    if not active_tower_run:
        raise HTTPException(status_code=404, detail="Nível da torre não encontrado!")
    
    active_tower_run.active = True
    session.commit()
    return {"mensagem": "Nível da torre ativado com sucesso!",
            "Nível da torre": active_tower_run}

async def listActiveActiveTowerRun(session):
    active_tower_run = session.query(ActiveTowerRun).filter(ActiveTowerRun.active == True).all()
    return active_tower_run
