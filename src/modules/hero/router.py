from fastapi import APIRouter, Depends, HTTPException
import httpx
from src.modules.hero.service import listAllHeroes, createHero, addHeroPack, desativateHeroPack, activateHero, activateHeroPack, desativateHero, listHero,listActiveHero, listActiveHeroByName
from src.modules.user.service import verificate_token
from src.modules.hero.schemas import HeroSchemaUser
from src.modules.hero_pack.schemas import HeroPackSchema
from sqlalchemy.orm import Session
from src.common.dependencies import get_session

hero_routes = APIRouter(prefix="/heroes", tags=["heroes"])

@hero_routes.get("/")
async def hero():
    return {"mensagem": "Você acessou a rota de heróis!"}

@hero_routes.get("/list-all-heroes")
async def listHeroes():
    result = await listAllHeroes(10)
    return result

@hero_routes.get("/list/{id}")
async def ListHEro(id_hero: int, session: Session = Depends(get_session)):
    result = await listHero(id_hero=id_hero, session=session)
    return result

@hero_routes.post("/create-hero")
async def CreateHero(
    hero: HeroSchemaUser, 
    session: Session = Depends(get_session),
    user = Depends(verificate_token) 
):
    # 2. Você passa o usuário de verdade para a função
    result = await createHero(hero_schema_user=hero, session=session, user=user)
    return result

@hero_routes.patch("/desativate/{id}")
async def DesativateHero(id_hero: int, 
                            user = Depends(verificate_token),
                            session: Session = Depends(get_session)
                            ):
    result = await desativateHero(id_hero=id_hero, user=user, session=session)
    return result

@hero_routes.patch("/activate/{id}")
async def ActivateHero(id_hero: int, 
                            user = Depends(verificate_token),
                            session: Session = Depends(get_session)
                            ):
    result = await activateHero(id_hero=id_hero, user=user, session=session)
    return result

###################* Hero_pack routes *######################

@hero_routes.post("/create-hero-pack/{id_hero}")
async def AddHeroPack(
    hero_pack: HeroPackSchema,
    session: Session = Depends(get_session),
    user = Depends(verificate_token),
    id_hero = int
):
    result = await addHeroPack(hero_pack_schema=hero_pack, session=session, user=user, id_hero=id_hero)
    return result

@hero_routes.patch("/desativate-hero-pack/{id}")
async def DesativateHeroPack(id_hero_pack: int, 
                            user = Depends(verificate_token),
                            session: Session = Depends(get_session)
                            ):
    result = await desativateHeroPack(id_hero_pack=id_hero_pack, user=user, session=session)
    return result

@hero_routes.patch("/activate-hero-pack/{id}")
async def ActivateHeroPack(id_hero_pack: int, 
                            user = Depends(verificate_token),
                            session: Session = Depends(get_session)
                            ):
    result = await activateHeroPack(id_hero_pack=id_hero_pack, user=user, session=session)
    return result

@hero_routes.get("/list-active")
async def ListActiveHero(session: Session = Depends(get_session)):
    result = await listActiveHero(session=session)
    return result

@hero_routes.get("/list-active-name/{name_hero}")
async def ListActiveHerpByName(name_hero: str, session: Session = Depends(get_session)):
    result = await listActiveHeroByName(session=session, name_hero=name_hero)
    return result