import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from src.common.dependencies import get_session, verificate_token
from sqlalchemy.orm import Session
from src.modules.user_hero.models import UserHero
from src.modules.hero_pack.models import HeroPack
from src.modules.active_tower_run.models import ActiveTowerRun
from src.modules.user.schemas import UserSchema, LoginSchema
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from src.core.config import bcrypt_context, ACESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm
from collections import defaultdict
import random

def addHero(session, user_hero_schema, id_hero, id_user):    

    new_user_hero = {
        "hero": id_hero,
        "user": id_user,
        "level": 1,
        "fragments": 0,
        "active": True
    }
    
    final_hero_uder_pack = UserHero(**new_user_hero)
    session.add(final_hero_uder_pack)
    session.commit()
    session.refresh(final_hero_uder_pack)
    return {"mensagem": f"Herói de usuário cadastrado com sucesso!"}

def AddFragmentsHero(session, id_hero, id_user):
    user_hero = session.query(UserHero).filter(UserHero.hero == id_hero, UserHero.user == id_user).first()
    if not user_hero:
        raise HTTPException(status_code=404, detail="Usuário de herói não encontrado!")
    fragments = user_hero.fragments + 1
    level = user_hero.level
    match fragments:
        case x if x >= 5 :
            if level < 2:
                user_hero.level = 2
                return {"mensagem": "Você subiu de nível para o nível 2!"}
        case x if 5 < x >= 10:
            if level < 3:
                user_hero.level = 3
                return {"mensagem": "Você subiu de nível para o nível 3!"}
        case x if 10 < x >= 25:
            if level < 4:
                user_hero.level = 4
                return {"mensagem": "Você subiu de nível para o nível 4!"}
        case x if 25 < x >= 50:
            if level < 5:
                user_hero.level = 5
                return {"mensagem": "Você subiu de nível para o nível 5!"}
        case x if 50 < x >= 100:
            if level < 6:
                user_hero.level = 6
                return {"mensagem": "Você subiu de nível para o nível 6!"}
        case x if 100 < x >= 250:
            if level < 7:
                user_hero.level = 7
                return {"mensagem": "Você subiu de nível para o nível 7!"}
    user_hero.fragments = fragments
    session.commit()
