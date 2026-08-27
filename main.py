from fastapi import FastAPI
# Importe o roteador do arquivo que você criou (ajuste o nome do arquivo aqui)
# from src.modules.comic_vine import router 
from src.modules.comic_vine import router
from src.modules.hero.router import hero_routes
from src.modules.pack.router import pack_routes
from src.modules.user.router import user_routes
from src.modules.class_hero.router import class_routes
from src.modules.hyper_attack.router import hyper_attack_routes
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import os
from src.core.database import engine, Base

load_dotenv()

app = FastAPI()

app.include_router(router)
app.include_router(hero_routes)
app.include_router(pack_routes)
app.include_router(user_routes)
app.include_router(class_routes)
app.include_router(hyper_attack_routes)

# 1. Importe TODOS os seus modelos aqui no main.py
from src.modules.user.models import User
from src.modules.active_tower_run.models import ActiveTowerRun
# from src.modules.hero.models import Hero (se tiver)

# 2. Crie as tabelas AQUI, logo após as importações
Base.metadata.create_all(bind=engine)

