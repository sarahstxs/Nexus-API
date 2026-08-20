from fastapi import FastAPI
# Importe o roteador do arquivo que você criou (ajuste o nome do arquivo aqui)
from src.modules.hero.comic_vine import router 
from src.modules.hero.models import hero_router

app = FastAPI()

# É esta linha que faz a aba aparecer no /docs!
app.include_router(router)
app.include_router(hero_router)