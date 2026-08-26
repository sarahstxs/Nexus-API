from fastapi import FastAPI
# Importe o roteador do arquivo que você criou (ajuste o nome do arquivo aqui)
# from src.modules.comic_vine import router 
from src.modules.comic_vine import router
from src.modules.hero.router import hero_routes

app = FastAPI()

# É esta linha que faz a aba aparecer no /docs!
app.include_router(router)
app.include_router(hero_routes)