from fastapi import HTTPException
from src.modules.user_hero.models import UserHero
from src.modules.hero.models import Hero

async def listAllHeroes(session, page: int, limit: int, id_user: int):
    offset = (page - 1) * limit
    
    heroes_db = session.query(UserHero)\
        .filter(UserHero.user == id_user)\
        .offset(offset)\
        .limit(limit)\
        .all()

    lista_herois = []
    
    for user_hero in heroes_db:
        hero = session.query(Hero).filter(Hero.id == user_hero.hero).first()
        
        if hero:

            lista_herois.append({
                "id": hero.id,
                "imageUrl": hero.image_hero
            })

    return {
        "page": page,
        "limit": limit,
        "heroes": lista_herois 
    }
def addHero(session, id_hero, id_user): 
    hero = session.query(Hero).filter(Hero.id == id_hero).first()
    if not hero:
        return

    new_user_hero = UserHero(
        hero=id_hero,
        user=id_user,
        current_hp=hero.base_hp,
        max_hp=hero.base_hp,
        drawback=None,
        alive=True,
        level=1,
        fragments=0,
        active=True
    )
    
    session.add(new_user_hero)
    session.flush()

def AddFragmentsHero(session, id_hero, id_user):
    user_hero = session.query(UserHero).filter(UserHero.hero == id_hero, UserHero.user == id_user).first()

    if not user_hero:
        return
    
    user_hero.fragments += 1
    fragments = user_hero.fragments
    level = user_hero.level

    if fragments >= 250 and level < 7:
        user_hero.level = 7
    elif fragments >= 100 and level < 6:
        user_hero.level = 6
    elif fragments >= 50 and level < 5:
        user_hero.level = 5
    elif fragments >= 25 and level < 4:
        user_hero.level = 4
    elif fragments >= 10 and level < 3:
        user_hero.level = 3
    elif fragments >= 5 and level < 2:
        user_hero.level = 2

    session.flush()

async def loseHealth(
        session, 
        id_hero, 
        id_user, 
        damage):
    user_hero = session.query(UserHero).filter(UserHero.hero == id_hero, UserHero.user == id_user).first()

    if not user_hero:
        raise HTTPException(
            status_code=404, 
            detail="Hero not found on user account!")
    
    user_hero.current_hp -= damage
    if user_hero.current_hp <= 0:
        user_hero.current_hp = 0
        user_hero.alive = False
        session.commit()
        return {"message": f"User took {damage} damage and died!"}

    session.commit()
    return {"message": f"User took {damage} damage!"}

async def acquireHealth(
        session, 
        id_hero, 
        id_user, 
        health):
    user_hero = session.query(UserHero).filter(UserHero.hero == id_hero, UserHero.user == id_user).first()

    if not user_hero:
        raise HTTPException(
            status_code=404, 
            detail="Hero not found on user account!")
    
    user_hero.current_hp += health
    if user_hero.current_hp >= user_hero.max_hp:
        user_hero.current_hp = user_hero.max_hp
        session.commit()
        return {"message": f"User recovered {health} health points and is at maximum health!"}

    session.commit()
    return {"message": f"User recovered {health} health points!"}

async def reviveHero(
        session, 
        id_hero, 
        id_user):
    user_hero = session.query(UserHero).filter(UserHero.hero == id_hero, UserHero.user == id_user).first()

    if not user_hero:
        raise HTTPException(
            status_code=404, 
            detail="Hero not found on user account!")
    
    user_hero.current_hp = user_hero.max_hp
    user_hero.alive = True
    session.commit()
    return {"message": "Hero resurrected with maximum health!"}