from fastapi import APIRouter, Depends, HTTPException
from src.modules.deck.service import createDeck, listAllDecks, listDeck, listDecksByUser, listDeckByUser, listActiveDecks, activateDeck, desativateDeck, listActiveDecksByUser, saveUserDeck
from src.modules.user.service import verificate_token
from sqlalchemy.orm import Session
from src.common.dependencies import get_session
from src.modules.deck.models import Deck


deck_routes = APIRouter(prefix="/decks", tags=["decks"])
#
@deck_routes.get("/")
async def deck():
    return {"mensagem": "Você acessou a rota de Decks!"}

@deck_routes.post("/")
async def CreateDeck(
    id_user: int,
    id_hero1: int,
    id_hero2: int,
    id_hero3: int,
    id_hero4: int,
    id_hero5: int,
    id_hero6: int,
    session: Session = Depends(get_session)
    ):
    result = await createDeck(
        id_user=id_user,
        id_hero1=id_hero1,
        id_hero2=id_hero2,
        id_hero3=id_hero3,
        id_hero4=id_hero4,
        id_hero5=id_hero5,
        id_hero6=id_hero6,
        session=session)
    return result

@deck_routes.get("/list")
async def ListAllDecks(
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
    ):
    result = await listAllDecks(
        session=session,
        user=user)
    return result

@deck_routes.get("/list/{id}")
async def ListDeck(
    id: int,  # Mudado de id_deck para id para casar com o Retrofit
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
):
    result = await listDeck(
        id_deck=id,  # Passando para a função auxiliar
        session=session,
        user=user
    )
    return result

async def listDeck(session, id_deck, user):
    deck = session.query(Deck).filter(Deck.id == id_deck).first()
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    
    # Validação correta de permissão (dono do deck ou admin)
    if deck.user_id != user.id and not user.admin:
        raise HTTPException(status_code=403, detail="Permission denied")
        
    return deck

@deck_routes.get("/list-decks")
async def ListDecksByUser(
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
    ):
    result = await listDecksByUser(
        session=session,
        user=user)
    return result

@deck_routes.get("/list-user-decks")
async def ListUserDecks(
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
):
    result = await listDecksByUser(
        session=session,
        user=user
    )
    return result

@deck_routes.patch("/desativate/{id}")
async def DesativateDeck(
    id_deck: int,
    id_user: int,
    session: Session = Depends(get_session)
    ):
    result = await desativateDeck(
        id_deck=id_deck,
        session=session,
        id_user=id_user)
    return result

@deck_routes.patch("/activate/{id}")
async def ActivateDeck(
    id_deck: int,
    id_user: int,
    session: Session = Depends(get_session)
    ):
    result = await activateDeck(
        id_deck=id_deck,
        session=session,
        id_user=id_user)
    return result

@deck_routes.get("/list-active")
async def ListActiveClass(
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
    ):
    result = await listActiveDecks(
        session=session,
        user=user)
    return result

@deck_routes.get("/list-active-by-user")
async def ListActiveClassByUser(
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
    ):
    result = await listActiveDecksByUser(
        session=session,
        user=user)
    return result

@deck_routes.post("/save-deck")
async def SaveUserDeck(
    id_hero1: int,
    id_hero2: int,
    id_hero3: int,
    id_hero4: int,
    id_hero5: int,
    id_hero6: int,
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
):
    result = await saveUserDeck(
        session=session,
        user=user,
        id_hero1=id_hero1,
        id_hero2=id_hero2,
        id_hero3=id_hero3,
        id_hero4=id_hero4,
        id_hero5=id_hero5,
        id_hero6=id_hero6
    )
    return result
