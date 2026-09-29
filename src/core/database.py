import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Carrega o arquivo .env
load_dotenv()

# Pega a URL de forma segura
DATABASE_URL = os.getenv("DATABASE_URL")

# Cria a conexão com o banco
engine = create_engine(DATABASE_URL)

# Alias para manter a compatibilidade com arquivos que importam 'db'
db = engine

# Cria a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria a Base para os modelos
Base = declarative_base()

# Função de sessão para as rotas e dependências
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()