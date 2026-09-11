from fastapi import Depends, HTTPException
from src.common.dependencies import get_session, verificate_token
from sqlalchemy.orm import Session
from src.modules.user.models import User
from src.modules.pack.models import Pack
from src.modules.hero.models import Hero
from src.modules.user_hero.models import UserHero
from src.modules.hero_pack.models import HeroPack
from src.modules.user_hero.service import addHero, AddFragmentsHero
from src.modules.active_tower_run.models import ActiveTowerRun
from src.modules.user.schemas import UserSchema, LoginSchema
from src.modules.user_hero.schemas import UserHeroSchema
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from src.core.config import bcrypt_context, ACESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm
import random

load_dotenv()

def create_token(
        id_user: str, 
        duration_token: int = timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + duration_token
    dic_info = {"sub": str(id_user), "exp": expiration_date}
    jwt_encoded = jwt.encode(dic_info, SECRET_KEY, ALGORITHM )

    return jwt_encoded

def autenticate_user(
        email: str, 
        password:str, 
        session):
    user = session.query(User).filter(User.email == email).first()

    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user 

def sortedHeros(
        session, 
        user_hero_schema, 
        id_pack, 
        id_user):
    heroes = session.query(HeroPack).filter(HeroPack.pack == id_pack).all()
    
    heroes_common = []
    heroes_rare = []
    heroes_legendary = []

    for hero in heroes:
        hero_complete = session.query(Hero).filter(Hero.id == hero.hero).first()

        match hero_complete.rarity:
            case 1:
                heroes_common.append(hero_complete)
            case 2:
                heroes_rare.append(hero_complete)
            case 3:
                heroes_legendary.append(hero_complete)

    heroes_selected = []
    for i in range(4):
        choice = int((random.random())*100)
        if choice >= 50:
            hero = random.choice(heroes_common)
        if 11 <= choice <= 49:
            hero = random.choice(heroes_rare)
        if choice <= 10:
            hero = random.choice(heroes_legendary)
        
        heroes_selected.append(hero.name)
        user_hero = session.query(UserHero).filter(UserHero.hero == hero.id, UserHero.user == id_user).first()
        if user_hero is None:
            addHero(
                session=session, 
                id_hero=hero.id, 
                id_user=id_user, 
                user_hero_schema=user_hero_schema)
        else:
            AddFragmentsHero(
                session=session, 
                id_hero=user_hero.hero, 
                id_user=user_hero.user)
    return heroes_selected

async def createUser(
        user_schema: UserSchema, 
        session = Depends(get_session)):

    userEmail = session.query(User).filter(User.email == user_schema.email).first()
    userUsername = session.query(User).filter(User.username == user_schema.username).first()

    if userEmail:
        # Já existe usuário om esse e-mail nessa sessão
        raise HTTPException(
            status_code=400, 
            detail="Email already registered!")
    if userUsername:
        # Já existe usuário com esse username nessa sessão
        raise HTTPException(
            status_code=400, 
            detail="Username already registered!")
    else:
        password = user_schema.password
        encrypted_password = bcrypt_context.hash(password)
        new_user = User(
            username=user_schema.username,
            password=encrypted_password,
            phone=user_schema.phone,
            email=user_schema.email,
            admin=user_schema.admin,
            active=user_schema.active,
            highest_level=user_schema.highest_level,
            coins=user_schema.coins,
            create_date=user_schema.create_date,
            current_level=user_schema.current_level
        )
        session.add(new_user)
        session.commit()
        return {"message": f"User {user_schema.username} registered successfully!"}
    
async def login(
        login_schema: LoginSchema, 
        session = Depends(get_session)):
    user = autenticate_user(login_schema.email,login_schema.password, session)

    if not user:
        raise HTTPException(
            status_code=400, 
            detail= "User not found or invalid credentials!")
    else:
        access_token = create_token(str(user.id))
        refresh_token = create_token(str(user.id), duration_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    
async def loginForm(
        data_form: OAuth2PasswordRequestForm = Depends(), 
        session: Session = Depends(get_session)):
    user = autenticate_user(data_form.username, data_form.password, session)

    if not user:
        raise HTTPException(
            status_code=400, 
            detail= "User not found or invalid credentials!")
    else:
        access_token = create_token(str(user.id))
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    
async def use_refresh_token(
        user: User = Depends(verificate_token)):
    access_token = create_token(str(user.id))
    return {
            "access_token": access_token,
            "token_type": "Bearer"
        }

async def listActiveUser(
        session):
    user = session.query(User).filter(User.active == True).all()
    return user

async def listActiveHyperAttackByName(
        session, 
        name_user):
    user = session.query(User).filter(
        User.username.icontains(name_user),
        User.active == True
    ).all()
    
    return user

async def listAllUsers(
        session, 
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to list users!")
    
    list = session.query(User).all()
    return {"Users": list}

async def listUSer(
        session, 
        id_user, 
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to list user!")
    
    user = session.query(User).filter(User.id == id_user).first()
    return user

async def upHighestLevel(
        session, 
        id_user, 
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403, 
            detail="You don't have permission to promote users!")
    
    user = session.query(User).filter(User.id == id_user).first()
    next_level = user.highest_level + 1
    level = session.query(ActiveTowerRun).filter(ActiveTowerRun.current_floor == next_level).first()
    if level:
        user.highest_level = next_level
        session.commit()
        return {"message": "User has reached the maximum level!"}
    return {"message": "User is already at the highest maximum level!"}

async def upCurrentLevel(
        session, 
        id_user, 
        user):
    if not user.admin:
        raise HTTPException(
            status_code=403, 
            detail="You don't have permission to promote users!")
    
    user = session.query(User).filter(User.id == id_user).first()
    next_level = user.current_level + 1
    level = session.query(ActiveTowerRun).filter(ActiveTowerRun.current_floor == next_level).first()
    if level:
        user.current_level = next_level
        session.commit()
        return {"message": "User promoted successfully!"}
    return {"message": "User is already at the highest level!"}

async def downCurrentLevel(
        session, 
        id_user, 
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403, 
            detail="You don't have permission to demote this user!")
    
    user = session.query(User).filter(User.id == id_user).first()
    user.current_level = 1
    session.commit()
    return {"message": "User demoted successfully!"}

async def giveCoins(
        session, 
        id_user, 
        user, 
        coins):
    
    if not user.admin:
        raise HTTPException(
            status_code=403, 
            detail="You don't have permission to grant coins to this user!")
    
    user = session.query(User).filter(User.id == id_user).first()
    user.coins += coins
    session.commit()
    return {"message": f"User received {coins} coins successfully!"}

async def removeCoins(
        session, 
        id_user, 
        user, 
        coins):
    if not user.admin:
        raise HTTPException(
            status_code=403, 
            detail="You don't have permission to deduct coins from this user!")
    
    user = session.query(User).filter(User.id == id_user).first()
    
    if user.coins < coins:
        return {"message": "User does not have enough coins!"}
    user.coins -= coins
    session.commit()
    return {"message": f"User lost {coins} coins successfully!"} 
    
async def desativateUser(
        session, 
        id_user, 
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to deactivate this user!")
    
    user = session.query(User).filter(User.id == id_user).first()

    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found!")
    
    user.active = False
    session.commit()
    return {"message": "User deactivated successfully!",
            "User": user}

async def activateUser(
        session, 
        id_user, 
        user):
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to activate this user!")
    
    user = session.query(User).filter(User.id == id_user).first()

    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found!")
    
    user.active = True
    session.commit()
    return {"message": "User activated successfully!",
            "User": user}

async def buyPack(
        session, 
        id_user, 
        id_pack, 
        user_hero_schema=UserHeroSchema):
    user = session.query(User).filter(User.id == id_user).first()
    pack = session.query(Pack).filter(Pack.id == id_pack).first()

    if user.coins >= pack.price:
        user.coins -= pack.price
        session.commit()
        return sortedHeros(
            session, 
            user_hero_schema=user_hero_schema, 
            id_pack=id_pack, 
            id_user=id_user)
        
    return{"message": "You do not have enough coins!"}
