from fastapi import HTTPException
from src.modules.class_hero.models import ClassHero
from dotenv import load_dotenv

load_dotenv()

async def listAllClasses(
        session):
    list = session.query(ClassHero).all()
    return {"Classes": list}

async def listClass(
        session,
        id_class):
    class_hero = session.query(ClassHero).filter(ClassHero.id == id_class).first()
    return class_hero

async def createClass(
        session,
        class_schema,
        user):
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to create classes!")
    
    name = class_schema.name,
    special_attack_effect = class_schema.special_attack_effect
    special_attack_name = class_schema.special_attack_name
    required_energy = class_schema.required_energy
    active = class_schema.active

    new_class = {
        "name": name,
        "special_attack_effect": special_attack_effect,
        "special_attack_name": special_attack_name,
        "required_energy": required_energy,
        "active": active
    }
    
    final_class = ClassHero(**new_class)
    session.add(final_class)
    session.commit()
    session.refresh(final_class)
    return {"message": f"Class registered successfully!"}

async def desativateClass(
        session,
        id_class,
        user):
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to deactivate this class!")
    
    class_hero = session.query(ClassHero).filter(ClassHero.id == id_class).first()

    if not class_hero:
        raise HTTPException(
            status_code=404,
            detail="Class not found!")
    
    class_hero.active = False
    session.commit()
    return {"message": "Class deactivated successfully!",
            "Class": class_hero}

async def activateClass(
        session,
        id_class,
        user):
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to activate this class!")
    
    class_hero = session.query(ClassHero).filter(ClassHero.id == id_class).first()

    if not class_hero:
        raise HTTPException(status_code=404, detail="Class not found!")
    
    class_hero.active = True
    session.commit()
    return {"message": "Class activated successfully!",
            "Class": class_hero}

async def listActiveClass(
        session):
    class_hero = session.query(ClassHero).filter(ClassHero.active == True).all()
    return class_hero

async def listActiveClassByName(
        session,
        name_class):
    class_hero = session.query(ClassHero).filter(
        ClassHero.name.icontains(name_class),
        ClassHero.active == True
    ).all()
    
    return class_hero