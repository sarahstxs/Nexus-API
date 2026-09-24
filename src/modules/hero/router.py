from fastapi import APIRouter, Depends, Query
from src.modules.hero.service import listAllHeroes, createHero, addHeroPack, desativateHeroPack, activateHero, activateHeroPack, desativateHero, listHero,listActiveHero, listActiveHeroByName, listActiveHeroById, listHeroComplete
from src.modules.user.service import verificate_token
from src.modules.hero.schemas import HeroSchemaUser
from src.modules.hero_pack.schemas import HeroPackSchema
from sqlalchemy.orm import Session
from src.common.dependencies import get_session
import traceback
from src.modules.hero.models import Hero
from src.modules.user_hero.models import UserHero
from fastapi import HTTPException


hero_routes = APIRouter(prefix="/heroes", tags=["heroes"])

@hero_routes.get("/")
async def hero():
    return {"mensagem": "Você acessou a rota de heróis!"}

@hero_routes.get("/list-all-heroes")
async def list_heroes(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1)
):
    # Repassa os parâmetros de paginação para a sua função de negócio
    result = await listAllHeroes(page=page, limit=limit, session=session)
    
    return result

@hero_routes.get("/list/{id}")
async def ListHero(
    id_hero: int,
    session: Session = Depends(get_session)
    ):
    result = await listHero(
        id_hero=id_hero,
        session=session)
    return result

@hero_routes.get("/list-complete-user-hero/{id_hero}/{id_user}")
def ListUserHero(
    id_hero: int,
    id_user: int,
    session: Session = Depends(get_session)
):
    try:
        have = False

        # Busca o herói
        hero = session.query(Hero).filter(Hero.id == id_hero).first()

        # Busca a relação do usuário com o herói
        user_hero = session.query(UserHero).filter(
            (UserHero.hero == id_hero) & (UserHero.user == id_user)
        ).first()

        # Função auxiliar para limpar os dados do SQLAlchemy e evitar erro de JSON
        def model_to_dict(obj):
            if not obj:
                return None
            # Remove chaves internas do SQLAlchemy (como _sa_instance_state)
            return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}

        hero_dict = model_to_dict(hero)
        user_hero_dict = model_to_dict(user_hero)

        if not user_hero:
            return {
                "hero": hero_dict,
                "have": have
            }
        else:
            have = True
            return {
                "hero": hero_dict,
                "user_hero": user_hero_dict,
                "have": have
            }

    except Exception as e:
        # Força o erro a aparecer no terminal com o traceback completo
        traceback.print_exc()
        # Retorna o erro detalhado na resposta HTTP para você ler na hora
        raise HTTPException(status_code=500, detail=str(e))

@hero_routes.post("/create-hero")
async def CreateHero(
    hero: HeroSchemaUser, 
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
    ):
    result = await createHero(
        hero_schema_user=hero,
        session=session,
        user=user)
    return result

@hero_routes.patch("/desativate/{id}")
async def DesativateHero(
    id_hero: int, 
    user = Depends(verificate_token),
    session: Session = Depends(get_session)
    ):
    result = await desativateHero(
        id_hero=id_hero,
        user=user,
        session=session)
    return result

@hero_routes.patch("/activate/{id}")
async def ActivateHero(
    id_hero: int, 
    user = Depends(verificate_token),
    session: Session = Depends(get_session)
    ):
    result = await activateHero(
        id_hero=id_hero,
        user=user,
        session=session)
    return result

###################* Hero_pack routes *######################

@hero_routes.post("/create-hero-pack/{id_hero}")
async def AddHeroPack(
    hero_pack: HeroPackSchema,
    session: Session = Depends(get_session),
    user = Depends(verificate_token),
    id_hero = int
    ):
    result = await addHeroPack(
        hero_pack_schema=hero_pack,
        session=session,
        user=user,
        id_hero=id_hero)
    return result

@hero_routes.patch("/desativate-hero-pack/{id}")
async def DesativateHeroPack(
    id_hero_pack: int, 
    user = Depends(verificate_token),
    session: Session = Depends(get_session)
    ):
    result = await desativateHeroPack(
        id_hero_pack=id_hero_pack,
        user=user,
        session=session)
    return result

@hero_routes.patch("/activate-hero-pack/{id}")
async def ActivateHeroPack(
    id_hero_pack: int, 
    user = Depends(verificate_token),
    session: Session = Depends(get_session)
    ):
    result = await activateHeroPack(
        id_hero_pack=id_hero_pack,
        user=user,
        session=session)
    return result

@hero_routes.get("/list-active")
async def ListActiveHero(
    session: Session = Depends(get_session)
    ):
    result = await listActiveHero(
        session=session)
    return result

@hero_routes.get("/list-active-name/{name_hero}")
async def ListActiveHerpByName(
    name_hero: str,
    session: Session = Depends(get_session)
    ):
    result = await listActiveHeroByName(
        session=session,
        name_hero=name_hero)
    return result

@hero_routes.get("/list-active-id/{id_hero}")
async def ListActiveHerpById(
    name_hero: str,
    session: Session = Depends(get_session)
    ):
    result = await listActiveHeroById(
        session=session,
        name_hero=name_hero)
    return result