from fastapi import HTTPException
from src.modules.active_tower_run.models import ActiveTowerRun

async def listAllActiveTowerRun(
        session):
    list = session.query(ActiveTowerRun).all()
    return {"Levels of the tower": list}

async def listActiveTowerRun(
        session,
        id_active_tower_run):
    active_tower_run = session.query(ActiveTowerRun).filter(ActiveTowerRun.id == id_active_tower_run).first()
    return active_tower_run

async def createActiveTowerRun(
        session,
        active_tower_run_schema,
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to create tower levels!")
    
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
    return {"message": f"Tower level registered successfully!"}

async def desativateActiveTowerRun(
        session,
        id_active_tower_run,
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to deactivate tower levels!")
    
    active_tower_run = session.query(ActiveTowerRun).filter(ActiveTowerRun.id == id_active_tower_run).first()

    if not active_tower_run:
        raise HTTPException(
            status_code=404,
            detail="Tower level not found!")
    
    active_tower_run.active = False
    session.commit()
    return {"message": "Tower level deactivated successfully!",
            "Level of the tower": active_tower_run}

async def activateActiveTowerRun(
        session,
        id_active_tower_run,
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to activate this tower level!")
    
    active_tower_run = session.query(ActiveTowerRun).filter(ActiveTowerRun.id == id_active_tower_run).first()

    if not active_tower_run:
        raise HTTPException(
            status_code=404,
            detail="Tower level not found!")
    
    active_tower_run.active = True
    session.commit()
    return {"mensagem": "Tower level activated successfully!",
            "Level of the tower": active_tower_run}

async def listActiveActiveTowerRun(
        session):
    active_tower_run = session.query(ActiveTowerRun).filter(ActiveTowerRun.active == True).all()
    return active_tower_run
