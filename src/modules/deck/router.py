from fastapi import APIRouter, Depends
from src.modules.deck.service import createDeck, listAllDecks, listDeck, listDecksByUser, listDeckByUser, listActiveDecks, activateDeck, desativateDeck, listActiveDecksByUser
from src.modules.user.service import verificate_token
from sqlalchemy.orm import Session
from src.common.dependencies import get_session

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
    session: Session = Depends(get_session)):
    result = await createDeck(
        id_user=id_user,
        id_hero1=id_hero1,
        id_hero2=id_hero2,
        id_hero3=id_hero3,
        id_hero4=id_hero4,
        session=session)
    return result

@deck_routes.get("/list")
async def ListAllDecks(
    session: Session = Depends(get_session),
    user = Depends(verificate_token) ):
    result = await listAllDecks(
        session=session,
        user=user)
    return result

@deck_routes.get("/list/{id}")
async def ListDeck(
    id_deck: int,
    session: Session = Depends(get_session),
    user = Depends(verificate_token)):
    result = await listDeck(
        id_deck=id_deck,
        session=session,
        user=user)
    return result

@deck_routes.get("/list-decks")
async def ListDecksByUser(
    session: Session = Depends(get_session),
    user = Depends(verificate_token) ):
    result = await listDecksByUser(
        session=session,
        user=user)
    return result

@deck_routes.get("/list-user/{id_deck}")
async def ListDeckByUser(
    id_deck: int,
    session: Session = Depends(get_session),
    user = Depends(verificate_token)):
    result = await listDeckByUser(
        id_deck=id_deck,
        session=session,
        user=user)
    return result

@deck_routes.patch("/desativate/{id}")
async def DesativateDeck(
    id_deck: int,
    id_user: int,
    session: Session = Depends(get_session)):
    result = await desativateDeck(
        id_deck=id_deck,
        session=session,
        id_user=id_user)
    return result

@deck_routes.patch("/activate/{id}")
async def ActivateDeck(
    id_deck: int,
    id_user: int,
    session: Session = Depends(get_session)):
    result = await activateDeck(
        id_deck=id_deck,
        session=session,
        id_user=id_user)
    return result

@deck_routes.get("/list-active")
async def ListActiveClass(
    session: Session = Depends(get_session),
    user = Depends(verificate_token)):
    result = await listActiveDecks(
        session=session,
        user=user)
    return result

@deck_routes.get("/list-active-by-user")
async def ListActiveClassByUser(
    session: Session = Depends(get_session),
    user = Depends(verificate_token)):
    result = await listActiveDecksByUser(
        session=session,
        user=user)
    return result
