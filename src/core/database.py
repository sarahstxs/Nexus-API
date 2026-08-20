import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType
from dotenv import load_dotenv

# Carrega o arquivo .env
load_dotenv()

# Pega a URL de forma segura
DATABASE_URL = os.getenv("DATABASE_URL")

db = create_engine(DATABASE_URL)

#Cria a conexão com o banco
Base = declarative_base()