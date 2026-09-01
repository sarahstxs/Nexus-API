from fastapi import HTTPException
from src.modules.user_hero.models import UserHero
from src.modules.hero.models import Hero

def addHero(
        session, 
        id_hero, 
        id_user):    
    hero = session.query(Hero).filter(Hero.id == id_hero).first()

    new_user_hero = {
        "hero": id_hero,
        "user": id_user,
        "current_hp": hero.base_hp,
        "max_hp": hero.base_hp,
        "drawback": None,
        "alive": True,
        "level": 1,
        "fragments": 0,
        "active": True
    }
    
    final_hero_uder_pack = UserHero(**new_user_hero)
    session.add(final_hero_uder_pack)
    session.commit()
    session.refresh(final_hero_uder_pack)
    return {"mensagem": f"Herói de usuário cadastrado com sucesso!"}

def AddFragmentsHero(session, 
                     id_hero, 
                     id_user):
    user_hero = session.query(UserHero).filter(UserHero.hero == id_hero, UserHero.user == id_user).first()
    hero = session.query(Hero).filter(Hero.id == id_hero).first()

    if not user_hero:
        raise HTTPException(status_code=404, detail="Usuário de herói não encontrado!")
    
    fragments = user_hero.fragments + 1
    level = user_hero.level

    match fragments:
        case x if x >= 5 :
            if level < 2:
                user_hero.level = 2
                user_hero.max_hp = user_hero.max_hp * 0.2
                return {"mensagem": "Você subiu de nível para o nível 2!"}
        case x if 5 < x >= 10:
            if level < 3:
                user_hero.level = 3
                user_hero.max_hp = user_hero.max_hp * 0.2
                return {"mensagem": "Você subiu de nível para o nível 3!"}
        case x if 10 < x >= 25:
            if level < 4:
                user_hero.level = 4
                user_hero.max_hp = user_hero.max_hp * 0.2
                return {"mensagem": "Você subiu de nível para o nível 4!"}
        case x if 25 < x >= 50:
            if level < 5:
                user_hero.level = 5
                user_hero.max_hp = user_hero.max_hp * 0.2
                return {"mensagem": "Você subiu de nível para o nível 5!"}
        case x if 50 < x >= 100:
            if level < 6:
                user_hero.level = 6
                user_hero.max_hp = user_hero.max_hp * 0.2
                return {"mensagem": "Você subiu de nível para o nível 6!"}
        case x if 100 < x >= 250:
            if level < 7:
                user_hero.level = 7
                user_hero.max_hp = user_hero.max_hp * 0.2
                return {"mensagem": "Você subiu de nível para o nível 7!"}
            
    user_hero.fragments = fragments
    session.commit()

async def loseHealth(
        session, 
        id_hero, 
        id_user, 
        damage):
    user_hero = session.query(UserHero).filter(UserHero.hero == id_hero, UserHero.user == id_user).first()

    if not user_hero:
        raise HTTPException(
            status_code=404, 
            detail="Herói não encontrado na conte da usuário!")
    
    user_hero.current_hp -= damage
    if user_hero.current_hp <= 0:
        user_hero.current_hp = 0
        user_hero.alive = False
        session.commit()
        return {"mensagem": f"O usuário perdeu {damage} pontos de vida e morreu!"}

    session.commit()
    return {"mensagem": f"O usuário perdeu {damage} pontos de vida!"}

async def acquireHealth(
        session, 
        id_hero, 
        id_user, 
        health):
    user_hero = session.query(UserHero).filter(UserHero.hero == id_hero, UserHero.user == id_user).first()

    if not user_hero:
        raise HTTPException(
            status_code=404, 
            detail="Herói não encontrado na conte da usuário!")
    
    user_hero.current_hp += health
    if user_hero.current_hp >= user_hero.max_hp:
        user_hero.current_hp = user_hero.max_hp
        session.commit()
        return {"mensagem": f"O usuário ganhou {health} pontos de vida e está com sua vida máxima!"}

    session.commit()
    return {"mensagem": f"O usuário ganhou {health} pontos de vida!"}

async def reviveHero(
        session, 
        id_hero, 
        id_user):
    user_hero = session.query(UserHero).filter(UserHero.hero == id_hero, UserHero.user == id_user).first()

    if not user_hero:
        raise HTTPException(
            status_code=404, 
            detail="Herói não encontrado na conte da usuário!")
    
    user_hero.current_hp = user_hero.max_hp
    user_hero.alive = True
    session.commit()
    return {"mensagem": "O herói ressuscitou com sua vida máxima"}