import os
import sys

# 1. Configura o sys.path PRIMEIRO
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

# 2. Agora importa a Base e os Models
from src.core.database import Base
from src.modules.active_tower_run import models
from src.modules.battle import models
from src.modules.class_hero import models
from src.modules.deck import models
from src.modules.deck_slot import models
from src.modules.hero import models
from src.modules.hero_pack import models
from src.modules.hyper_attack import models
from src.modules.pack import models
from src.modules.place import models
from src.modules.user import models
from src.modules.user_hero import models

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Adiciona o diretório raiz do projeto ao sys.path
from dotenv import load_dotenv  # <--- 1. Importe o load_dotenv

# Carrega as variáveis do arquivo .env localizado na raiz do projeto
load_dotenv()

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Objeto de configuração do Alembic
config = context.config

# Interpretador do arquivo de configuração de logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- 2. PEGUE A URL DO .ENV E INJETE NO CONFIG DO ALEMBIC ---
# Substitua 'DATABASE_URL' pelo nome exato da variável que está no seu .env
database_url = os.getenv("DATABASE_URL") 

if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# (Opcional) Importe o Base dos seus models caso vá usar --autogenerate
# from meu_projeto.models import Base
# target_metadata = Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
